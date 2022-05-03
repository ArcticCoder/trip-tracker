from db_connection import get_db_connection


class ProfileRepository:
    """Profiilien tallentamisesta vastaava luokka."""

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection:
                Aktiivinen tietokantayhteys Connection-oliona
        """
        self._connection = connection

    def list_all(self):
        """Etsii tietokannasta kaikki profiilit.

        Returns:
            Lista tupleja, jotka edustavat profiileja muodossa (id, nimi)
        """
        sql = "SELECT id, name FROM profiles ORDER BY name;"
        rows = self._connection.execute(sql).fetchall()
        return list(map(tuple, rows))

    def add(self, name: str):
        """Lisää tietokantaan profiilin, jos nimi on saatavilla.

        Args:
            name:
                Uuden profiilin nimi merkkijonona.
        """
        if self._name_available(name):
            sql = "INSERT INTO profiles (name) VALUES (?);"
            self._connection.execute(sql, [name])
            self._connection.commit()

    def remove(self, profile_id: int):
        """Poistaa profiilin tietokannasta.

        Args:
            profile_id:
                Profiilin id tietokannassa kokonaislukuna.
        """
        sql = "DELETE FROM profiles WHERE id = ?;"
        self._connection.execute(sql, [profile_id])
        self._connection.commit()

    def _name_available(self, name: str):
        sql = "SELECT name FROM profiles WHERE name = ?;"
        result = self._connection.execute(sql, [name]).fetchone()
        return result is None


profile_repository = ProfileRepository(get_db_connection())
