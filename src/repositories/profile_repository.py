from db_connection import get_db_connection

class ProfileRepository:
    def __init__(self, connection):
        self._connection = connection

    def list_all(self):
        sql = "SELECT id, name FROM profiles ORDER BY name"
        rows = self._connection.execute(sql).fetchall()
        return list(map(tuple, rows))

    def find_name(self, user_id : int):
        sql = "SELECT name FROM profiles WHERE id = ?"
        result = self._connection.execute(sql, [user_id]).fetchone()
        if result:
            return result[0]
        return None

    def find_id(self, name : str):
        sql = "SELECT id FROM profiles WHERE name = ?"
        result = self._connection.execute(sql, [name]).fetchone()
        if result:
            return result[0]
        return None

    def add(self, name : str):
        if self._name_available(name):
            sql = "INSERT INTO profiles (name) VALUES (?)"
            self._connection.execute(sql, [name])
            self._connection.commit()

    def remove(self, name : str):
        sql = "DELETE FROM profiles WHERE name==?"
        self._connection.execute(sql, [name])
        self._connection.commit()

    def _name_available(self, name : str):
        sql = "SELECT name FROM profiles WHERE name = ?"
        result = self._connection.execute(sql, [name]).fetchone()
        return result is None

profile_repository = ProfileRepository(get_db_connection())
