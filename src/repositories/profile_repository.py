from db_connection import get_db_connection

class ProfileRepository:
    def __init__(self, connection):
        self._connection = connection

    def list_all(self):
        rows = self._connection.execute("SELECT id, name FROM profiles ORDER BY name").fetchall()
        return list(map(tuple, rows))

    def find_name(self, id : int):
        result = self._connection.execute("SELECT name FROM profiles WHERE id = ?", [id]).fetchone()
        if result:
            return result[0]
        return None

    def find_id(self, name : str):
        result = self._connection.execute("SELECT id FROM profiles WHERE name = ?", [name]).fetchone()
        if result:
            return result[0]
        return None

    def add(self, name : str):
        if self._name_available(name):
            self._connection.execute("INSERT INTO profiles (name) VALUES (?)", [name])
            self._connection.commit()

    def remove(self, name : str):
        self._connection.execute("DELETE FROM profiles WHERE name==?", [name])
        self._connection.commit()

    def _name_available(self, name : str):
        result = self._connection.execute("SELECT name FROM profiles WHERE name = ?", [name]).fetchone()
        return result is None

profile_repository = ProfileRepository(get_db_connection())
