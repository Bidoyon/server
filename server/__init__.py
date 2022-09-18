from .application import Application
from .permissions import Permissions
from .response import Response
from .constants import *

app = Application()


@app.websocket_event("auth")
async def on_auth_request(websocket, name, password):
    if await app.connections.auth(websocket, name, password):
        return Response(True, message="auth-accepted")
    return Response(True, message="auth-refused")


@app.websocket_event("add-user", required_permissions=[Permissions.AddUser])
async def on_add_user_request(name: str, password: str):
    if app.data.get_user_by_name(name):
        return Response(False, reason="User already exists")
    id = app.data.add_user(name, password)
    return Response(True, user=app.data.get_user_by_id(id))


@app.websocket_event("remove-user", required_permissions=[Permissions.RemoveUser])
async def on_remove_user_request(id: int):
    if not app.data.get_user_by_id(id):
        return Response(False, reason="User does not exist")
    app.data.remove_user(id)
    app.data.reset_roles(id)
    app.data.set_investment(id, 0)
    app.data.move_containers_to(id, CommonUser)
    return Response(True)


@app.websocket_event("set-user-name", required_permissions=[Permissions.SetUserName])
async def on_set_user_name_request(id: int, name: str):
    if not app.data.get_user_by_id(id):
        return Response(False, reason="User does not exist")
    app.data.set_user_name(id, name)
    return Response(True)


@app.websocket_event("set-user-password", required_permissions=[Permissions.SetUserPassword])
async def on_set_user_password_request(id: int, password: str):
    if not app.data.get_user_by_id(id):
        return Response(False, reason="User does not exist")
    app.data.set_user_password(id, password)
    return Response(True)

