from fastapi import WebSocket
from .authentication import Authentication


class Connections:

    def __init__(self, app):
        self.app = app
        self.connections: list[WebSocket] = []
        self.authed: dict[WebSocket, Authentication] = {}

    def connect(self, websocket: WebSocket):
        self.connections.append(websocket)

    async def auth(self, websocket: WebSocket, name: str, password: str):
        auth = Authentication(self.app, name, password)
        if auth.valid:
            self.authed[websocket] = auth
            await self.app.emit("authentication", websocket=websocket, authentication=auth)
            return True
        return False

    def get_auth(self, websocket):
        try:
            return self.authed[websocket]
        except KeyError:
            return None

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
        if websocket in self.authed.keys():
            del self.authed[websocket]

    async def broadcast(self, event, args):
        for websocket in self.connections:
            await websocket.send_json({'event': event, 'args': args})
