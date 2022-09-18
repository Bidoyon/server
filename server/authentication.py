class Authentication:

    def __init__(self, app, name: str, password: str):
        self.app = app
        self.name = name

        self.valid = False

        user = app.data.get_user_by_name(name)
        if not user:
            return

        if not password == user["password"]:
            return

        self.roles = app.data.get_roles(user["id"])
        self.permissions = app.data.get_permissions(self.roles)

        self.valid = True
