from db_connection import get_db_connection
from entities.trip import Trip


class TripRepository:
    """Matkojen tallentamisesta vastaava luokka"""

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection:
                Aktiivinen tietokantayhteys Connection-oliona
        """
        self._connection = connection

    def find_by_profile(self, profile_id: int, start_time: str = None, end_time: str = None):
        """Etsii tietokannasta matkat profiilin id:n mukaan, haluttaessa tietyltä aikaväliltä.

        Args:
            profile_id:
                Profiilin id tietokannassa kokonaislukuna.
            start_time:
                Valinnainen, aikaisinta haluttua aikaa edustava merkkijono muodossa
                YYYY(-MM-DD HH:MM:SS), suluissa olevat valinnaisia.
            end_time:
                Valinnainen, viimeisintä haluttua aikaa edustava merkkijono muodossa
                YYYY(-MM-DD HH:MM:SS), suluissa olevat valinnaisia.

        Returns:
            Lista Trip-olioita aikajärjestyksessä.
        """
        if not start_time:
            # Kaikille mahd. merkkijonoille start_time >= ""
            start_time = ""
        if not end_time:
            # Kaikille valideille merkkijonoille end_time <= "A"
            end_time = "A"
        sql = "SELECT id, name, start_time, end_time,"\
            "strftime('%s', end_time)-strftime('%s', start_time) as duration,"\
            "length, length*1000/(strftime('%s', end_time)-strftime('%s', start_time)) FROM trips "\
            "WHERE profile_id = ? AND start_time >= ? AND end_time <= ? ORDER BY start_time;"
        rows = self._connection.execute(
            sql, [profile_id, start_time, end_time]).fetchall()
        ret = []
        for row in rows:
            ret.append(Trip(row["id"], row["name"], row["start_time"], row["end_time"],
                            row["duration"], row["length"]))
        return ret

    def add(self, profile_id: int, name: str, start_time: str, end_time: str, length: int):
        """Lisää matkan tietokantaan.

        Args:
            profile_id:
                Profiilin id tietokannassa kokonaislukuna.
            name:
                Matkan nimi merkkijonona.
            start_time:
                Matkan alkamisen aikaa edustava merkkijono muodossa
                YYYY-MM-DD HH:MM(:SS), suluissa olevat valinnaisia.
            end_time:
                Matkan lopumisen aikaa edustava merkkijono muodossa
                YYYY-MM-DD HH:MM(:SS), suluissa olevat valinnaisia.
            length:
                Matkan pituus metreinä kokonaislukuna.
        """
        if start_time > end_time:
            return
        if length < 0:
            return

        sql = "INSERT INTO trips (profile_id, name, start_time, end_time, length)"\
            "VALUES (?, ?, ?, ?, ?);"
        self._connection.execute(
            sql, [profile_id, name, start_time, end_time, length])
        self._connection.commit()

    def remove(self, trip_id: int):
        """Poistaa halutun matkan tietokannasta.

        Args:
            trip_id:
                Matkan id tietokannassa kokonaislukuna.
        """
        sql = "DELETE FROM trips WHERE id = ?;"
        self._connection.execute(sql, [trip_id])
        self._connection.commit()

    def remove_by_profile(self, profile_id: int):
        """Poistaa kaikki tietyn profiilin matkat tietokannasta.

        Args:
            profile_id:
                Profiilin id tietokannassa kokonaislukuna.
        """
        sql = "DELETE FROM trips WHERE profile_id = ?;"
        self._connection.execute(sql, [profile_id])
        self._connection.commit()


trip_repository = TripRepository(get_db_connection())
