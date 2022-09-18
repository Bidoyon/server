from sqlite3 import connect


def format_values(names, values):
    formatted = {}
    index = 0
    for value in values:
        formatted[names[index]] = value
        index += 1
    return formatted


class Database:

    def __init__(self):
        self.connection = connect("database.db")

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()

    def cursor(self):
        return self.connection.cursor()

    def basic_individual_select(self, columns, table, identifier_name, identifier):
        select = self.basic_select(columns, table, identifier_name, identifier)
        if select:
            return select[0]

    def basic_select(self, columns, table, identifier_name=None, identifier=None):
        cursor = self.cursor()
        if identifier_name and identifier:
            cursor.execute(f"SELECT {','.join(columns)} FROM {table} WHERE {identifier_name}=?", [identifier])
        else:
            cursor.execute(f"SELECT {','.join(columns)} FROM {table}")
        values = cursor.fetchall()
        select = []
        for value in values:
            select.append(format_values(columns, value))
        return select

