from db_connection import get_db_connection


class ProfileRepository:
    def __init__(self, connection):
        self._connection = connection

    def list_all(self):
        sql = "SELECT id, name FROM profiles ORDER BY name;"
        rows = self._connection.execute(sql).fetchall()
        return list(map(tuple, rows))

    def add(self, name: str):
        if self._name_available(name):
            sql = "INSERT INTO profiles (name) VALUES (?);"
            self._connection.execute(sql, [name])
            self._connection.commit()

    def remove(self, profile_id: int):
        sql = "DELETE FROM profiles WHERE id = ?;"
        self._connection.execute(sql, [profile_id])
        self._connection.commit()

    def _name_available(self, name: str):
        sql = "SELECT name FROM profiles WHERE name = ?;"
        result = self._connection.execute(sql, [name]).fetchone()
        return result is None


profile_repository = ProfileRepository(get_db_connection())
