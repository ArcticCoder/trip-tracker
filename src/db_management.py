from db_connection import get_db_connection

def drop_tables(connection):
    connection.execute("DROP TABLE IF EXISTS profiles;")

def create_tables(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS profiles"\
            "(id INTEGER PRIMARY KEY, name TEXT UNIQUE);")

def init_db():
    connection = get_db_connection()
    drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    init_db()
