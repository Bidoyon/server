from .constants import *

from .database import Database


class Data:

    def __init__(self, database: Database):
        with database as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS squeezes (id INTEGER PRIMARY KEY AUTOINCREMENT, fruits INTEGER, juice INTEGER)")
            cursor.execute("CREATE TABLE IF NOT EXISTS containers (id INTEGER PRIMARY KEY AUTOINCREMENT, owner INTEGER, capacity INTEGER, filling INTEGER)")
            cursor.execute("CREATE TABLE IF NOT EXISTS investments (user INTEGER PRIMARY KEY, fruits INTEGER)")
            cursor.execute("CREATE TABLE IF NOT EXISTS roles (user INTEGER, role TEXT, PRIMARY KEY (user, role))")
            cursor.execute("CREATE TABLE IF NOT EXISTS permissions (role TEXT, permission TEXT, PRIMARY KEY (role, permission))")
        self.database = database

    def get_user_by_id(self, id: int):
        return self.database.basic_individual_select(["id", "name", "password"], "users", "id", id)

    def get_user_by_name(self, name: str):
        return self.database.basic_individual_select(["id", "name", "password"], "users", "name", name)

    def add_user(self, name: str, password: str) -> int:
        with self.database as cursor:
            cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", [name, password])
        return self.get_user_by_name(name)["id"]

    def remove_user(self, id: int):
        with self.database as cursor:
            cursor.execute("DELETE FROM users WHERE id=?", [id])

    def set_user_name(self, id: int, name: str):
        with self.database as cursor:
            cursor.execute("UPDATE users SET name=? WHERE id=?", [name, id])

    def set_user_password(self, id: int, password: str):
        with self.database as cursor:
            cursor.execute("UPDATE users SET password=? WHERE id=?", [password, id])

    def get_squeezes(self):
        return self.database.basic_select(["id", "fruits", "juice"], "squeezes")

    def get_squeeze(self, id: int):
        return self.database.basic_individual_select(["id", "fruits", "juice"], "squeezes", "id", id)

    def add_squeeze(self):
        with self.database as cursor:
            cursor.execute("INSERT INTO squeezes (fruits, juice) VALUES (0, 0)")

    def remove_squeeze(self, id: int):
        with self.database as cursor:
            cursor.execute("DELETE FROM squeezes WHERE id=?", [id])

    def set_squeeze_fruits(self, id: int, fruits: int):
        with self.database as cursor:
            cursor.execute("UPDATE squeezes SET fruits=? WHERE id=?", [fruits, id])

    def add_squeeze_fruits(self, id: int, fruits: int):
        with self.database as cursor:
            cursor.execute("UPDATE squeezes SET fruits=fruits+? WHERE id=?", [fruits, id])

    def set_squeeze_juice(self, id: int, juice: int):
        with self.database as cursor:
            cursor.execute("UPDATE squeezes SET juice=? WHERE id=?", [juice, id])

    def add_squeeze_juice(self, id: int, juice: int):
        with self.database as cursor:
            cursor.execute("UPDATE squeezes SET juice=juice+? WHERE id=?", [juice, id])

    def get_containers(self):
        return self.database.basic_select(["id", "owner", "capacity", "filling"], "containers")

    def get_container(self, id: int):
        return self.database.basic_individual_select(["id", "owner", "capacity", "filling"], "containers", "id", id)

    def add_container(self, owner: int = CommonUser, capacity: int = DefaultContainerCapacity, filling: int = DefaultContainerFilling):
        with self.database as cursor:
            cursor.execute("INSERT INTO containers (owner, capacity, fillind) VALUES (?, ?, ?)", [owner, capacity, filling])

    def remove_container(self, id: int):
        with self.database as cursor:
            cursor.execute("DELETE FROM containers WHERE id=?", [id])

    def set_container_owner(self, id: int, owner: int = CommonUser):
        with self.database as cursor:
            cursor.execute("UPDATE containers SET owner=? WHERE id=?", [owner, id])

    def move_containers_to(self, old_owner: int, new_owner: int = CommonUser):
        with self.database as cursor:
            cursor.execute("UPDATE containers SET owner=? WHERE owner=?", [new_owner, old_owner])

    def set_container_capacity(self, id: int, capacity: int = DefaultContainerCapacity):
        with self.database as cursor:
            cursor.execute("UPDATE containers SET capacity=? WHERE id=?", [capacity, id])

    def set_container_filling(self, id: int, filling: int = DefaultContainerFilling):
        with self.database as cursor:
            cursor.execute("UPDATE containers SET filling=? WHERE id=?", [filling, id])

    def get_investment(self, user: int):
        return self.database.basic_individual_select(["fruits"], "investments", "user", user) or 0

    def set_investment(self, user: int, investment: int):
        with self.database as cursor:
            if investment > 0:
                cursor.execute("REPLACE INTO investments (user, fruits) VALUES (?, ?)", [user, investment])
            else:
                cursor.execute("DELETE FROM investments WHERE user=?", [user])

    def get_roles(self, user: int) -> list[str]:
        cursor = self.database.cursor()
        cursor.execute("SELECT role FROM roles WHERE user=?", [user])
        values = cursor.fetchall()
        roles = []
        for value in values:
            roles.append(value[0])
        return roles

    def set_roles(self, user: int, roles: list[str]):
        with self.database as cursor:
            self.reset_roles(user)
            for role in roles:
                self.add_role(user, role)

    def reset_roles(self, user: int):
        with self.database as cursor:
            cursor.execute("DELETE FROM roles WHERE user=?", [user])

    def add_role(self, user: int, role: str):
        with self.database as cursor:
            cursor.execute("INSERT INTO roles (user, role) VALUES (?, ?)", [user, role])

    def remove_role(self, user: int, role: str):
        with self.database as cursor:
            cursor.execute("DELETE FROM roles WHERE user=? AND role=?", [user, role])

    def get_permissions(self, roles: list[str]):
        if not roles:
            return []

        cursor = self.database.cursor()

        sql = "SELECT permission FROM permissions WHERE condition"
        condition = " OR ".join(map(lambda role: "role=" + role, roles))
        cursor.execute(sql.replace("condition", condition))

        values = cursor.fetchall()
        permissions = []
        for value in values:
            permissions.append(value[0])
        return permissions

    def set_permissions(self, role: str, permissions: list[str]):
        with self.database as cursor:
            cursor.execute("DELETE FROM permissions WHERE role=?", [role])
            for permission in permissions:
                self.add_permission(role, permission)

    def add_permission(self, role: str, permission: str):
        with self.database as cursor:
            cursor.execute("INSERT INTO permissions (role, permission) VALUES (?, ?)", [role, permission])

    def remove_permission(self, role: str, permission: str):
        with self.database as cursor:
            cursor.execute("DELETE FROM permissions WHERE role=? AND permission=?", [role, permission])
