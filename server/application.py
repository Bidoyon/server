import inspect

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .connections import Connections
from .data import Data
from .database import Database
from .logger import Logger
from .response import Response


class Application:

    def __init__(self):
        self.fastapi = FastAPI()
        self.connections = Connections(self)
        self.database = Database()
        self.logger = Logger("Bidoyon")
        self.data = Data(self.database)
        self.handlers = {}

        self.load_websockets()

    def load_websockets(self):
        @self.fastapi.websocket("/websockets")
        async def handler(websocket: WebSocket):
            await self.connect(websocket)

    def add_handler(self, event, function):
        if event in self.handlers:
            handlers = self.handlers[event]
        else:
            handlers = []

        async def handler(**args):
            params = args.copy()
            for arg in args.keys():
                if arg not in function.__code__.co_varnames:
                    del params[arg]
            if inspect.iscoroutinefunction(function):
                await function(**params)
            else:
                function(**params)

        handlers.append(handler)
        self.handlers[event] = handlers

    def add_websocket_handler(self, event, function, required_permissions, required_roles):
        if event in self.handlers:
            handlers = self.handlers[event]
        else:
            handlers = []

        async def handler(**args):
            if "code" not in args.keys():
                return

            if required_permissions and required_roles:
                auth = self.connections.get_auth(args["websocket"])
                if not auth:
                    await self.respond(args["websocket"], args["code"], False, reason="Socket is not authed")
                    return
                for permission in required_permissions:
                    if permission not in auth.permissions:
                        await self.respond(args["websocket"], args["code"], False, reason="Not enough permissions")
                        return
                for role in required_roles:
                    if role not in auth.roles:
                        await self.respond(args["websocket"], args["code"], False, reason="Role is missing")
                        return

            params = args.copy()
            for arg in args.keys():
                if arg not in function.__code__.co_varnames:
                    del params[arg]

            if inspect.iscoroutinefunction(function):
                result = await function(**params)
            else:
                result = function(**params)

            if result and isinstance(result, Response):
                await self.respond(args["websocket"], args["code"], result.success, **result.args)
                return

            await self.respond(args["websocket"], args["code"], False, reason="Processed but no response")

        handlers.append(handler)
        self.handlers[event] = handlers

    def event(self, event):
        def decorator(function):
            self.add_handler(event, function)
            return function

        return decorator

    def websocket_event(self, event, required_permissions=None, required_roles=None):
        if required_permissions is None:
            required_permissions = []
        if required_roles is None:
            required_roles = []

        def decorator(function):
            self.add_websocket_handler("ws-" + event, function, required_permissions, required_roles)
            return function

        return decorator

    async def emit(self, event, **args):
        if event not in self.handlers:
            return
        for handler in self.handlers[event]:
            await handler(**args)

    async def send(self, socket: WebSocket, event: str, **args):
        await socket.send_json({"event": event, "args": args})

    async def respond(self, socket: WebSocket, code: int, success: bool, **args):
        await self.send(socket, "response", code=code, success=success, **args)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.connect(websocket)
        await self.emit('connection', websocket=websocket)
        try:
            while True:
                data = await websocket.receive_json()
                await self.emit("ws-" + data['event'], websocket=websocket, **data['args'])
        except WebSocketDisconnect:
            self.connections.disconnect(websocket)
            await self.emit('disconnection', websocket=websocket)
