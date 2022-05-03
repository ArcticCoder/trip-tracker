from db_connection import get_db_connection


def drop_tables(connection):
    """Poistaa tietokantataulut.

    Args:
        connection: Connection-tyyppinen tietokantayhteys
    """
    connection.execute("DROP TABLE IF EXISTS profiles;")
    connection.execute("DROP TABLE IF EXISTS trips;")


def create_tables(connection):
    """Luo tietokantataulut.

    Args:
        connection: Connection-tyyppinen tietokantayhteys
    """
    connection.execute("CREATE TABLE IF NOT EXISTS profiles"
                       "(id INTEGER PRIMARY KEY, name TEXT UNIQUE);")
    connection.execute("CREATE TABLE IF NOT EXISTS trips"
                       "(id INTEGER PRIMARY KEY, profile_id INTEGER NOT NULL,"
                       "name TEXT NOT NULL, start_time TEXT, end_time TEXT,"
                       "length INTEGER,"
                       "FOREIGN KEY(profile_id) REFERENCES profiles(id));")


def init_db():
    """Alustaa tietokannan."""
    connection = get_db_connection()
    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    init_db()
