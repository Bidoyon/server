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


@app.websocket_event("add-squeeze", required_permissions=[Permissions.AddSqueeze])
async def on_add_squeeze_request():
    app.data.add_squeeze()
    return Response(True)


@app.websocket_event("remove-squeeze", required_permissions=[Permissions.RemoveSqueeze])
async def on_remove_squeeze_request(id: int):
    if not app.data.get_squeeze(id):
        return Response(False, reason="Squeeze does not exist")
    app.data.remove_squeeze(id)
    return Response(True)


@app.websocket_event("set-squeeze-fruits", required_permissions=[Permissions.SetSqueezeFruits])
async def on_set_squeeze_fruits_request(id: int, fruits: int):
    if not app.data.get_squeeze(id):
        return Response(False, reason="Squeeze does not exist")
    app.data.set_squeeze_fruits(id, fruits)
    return Response(True)


@app.websocket_event("set-squeeze-juice", required_permissions=[Permissions.SetSqueezeJuice])
async def on_set_squeeze_juice_request(id: int, juice: int):
    if not app.data.get_squeeze(id):
        return Response(False, reason="Squeeze does not exist")
    app.data.set_squeeze_juice(id, juice)
    return Response(True)


@app.websocket_event("add-container", required_permissions=[Permissions.AddContainer])
async def on_add_container_request(owner: int, capacity: int, filling: int):
    app.data.add_container(owner, capacity, filling)
    return Response(True)


@app.websocket_event("remove-container", required_permissions=[Permissions.RemoveContainer])
async def on_remove_container_request(id: int):
    if not app.data.get_container(id):
        return Response(False, reason="Container does not exist")
    app.data.remove_container(id)
    return Response(True)


@app.websocket_event("set-container-owner", required_permissions=[Permissions.SetContainerOwner])
async def on_set_container_owner_request(id: int, owner: int):
    if not app.data.get_container(id):
        return Response(False, reason="Container does not exist")
    app.data.set_container_owner(id, owner)
    return Response(True)


@app.websocket_event("set-container-capacity", required_permissions=[Permissions.SetContainerCapacity])
async def on_set_container_capacity_request(id: int, capacity: int):
    if not app.data.get_container(id):
        return Response(False, reason="Container does not exist")
    app.data.set_container_capacity(id, capacity)
    return Response(True)


@app.websocket_event("set-container-filling", required_permissions=[Permissions.SetContainerFilling])
async def on_set_container_filling_request(id: int, filling: int):
    if not app.data.get_container(id):
        return Response(False, reason="Container does not exist")
    app.data.set_container_filling(id, filling)
    return Response(True)
