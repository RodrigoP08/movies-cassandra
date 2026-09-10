from cassandra.cluster import Cluster
import uuid

# conectarse al cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
print('Se conecto bien a cassandra')


def create_keyspace_and_table(session):
    # Crearr keyspace
    CREATE_KEYSPACE = """
    CREATE KEYSPACE IF NOT EXISTS movies
    WITH replication = { 'class': 'SimpleStrategy','replication_factor':1}
    """
    session.execute(CREATE_KEYSPACE)
    session.set_keyspace("movies")


    # CREACION DE TABLAS
    CREATE_TABLE_MOVIE_BY_TITLE = """
    CREATE TABLE IF NOT EXISTS movies_by_title (movie_id UUID, title TEXT, release_year INT, genre TEXT, rating FLOAT, director TEXT,
                                          PRIMARY KEY ((title), release_year)
    )
    """
    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_TITLE)
    session.execute(stmt)
    print("Tabla creada: movies_by_title")


    CREATE_TABLE_MOVIE_BY_GENRE = """
    CREATE TABLE IF NOT EXISTS movies_by_genre (movie_id UUID, title TEXT, release_year INT, genre TEXT, rating FLOAT, director TEXT,
                                          PRIMARY KEY ((genre), rating)
    )
    """
    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_GENRE)
    session.execute(stmt)
    print("Tabla creada: movies_by_genre")
    pass:

# INSERTS ------------------------------------------------------------------------
def insert_movie(session, title, year, director, genre, rating, direcotr):
    INSERT_MOVIE_TITLE = """ 
    INSERT INTO movies_by_title(movie_id, title, release_year, genre, rating, director)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    movie_id = uuid.uuid4()
    stmt = session.prepare(INSERT_MOVIE_TITLE)   
    session.execute(stmt, (movie_id, title, year, genre, rating, director))


    INERT_MOVIES_GENRE = """
    INSERT INTO movies_by_genre(movie_id, title, release_year, genre, rating, director)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    movie_id = uuid.uuid4()
    stmt = session.prepare(INERT_MOVIES_GENRE)   
    session.execute(stmt, (movie_id, title, year, genre, rating, director))
    pass:
# ----------------------------------------------------------------------------------------
# CONSULTAR DATOS
# por titulo

def query_by_title(session, title, year):
    SELECT_BY_TITLE = "SELECT * FROM movies_by_title"
    stmt = session.prepare(SELECT_BY_TITLE)
    rows = session.execute(stmt)

    for r in rows:
        print(r.title, r.release_year, r.genre, r.rating, r.dierctor)
    pass:

def query_by_genre(session, genre):
# consylta por genero
    SELECT_BY_GENRE = "SELECT * FROM movies_by_genre"


# ----------------------------------------------------------------------------------------
# ACTUALIZAR DATAZOAOS
def update_movie_director(session, title, genre, new_director):
    UPDATE_MOVIE_DIRECTOR = """
    UPDATE movies_by_genre
    SET rating=?
    WHERE title=? AND genre=?
        AND dierctor=?
    """
    stmt = session.prepare(UPDATE_RATING)
    session.execute(stmt, (title, genre, new_director))
    pass:

def upadte_movie
# ELIMINAR DATOS
DELETE_MOVIE_TITLE = """
DELETE FROM movies_by_title
WHERE title=? AND release_year=?
    AND genre=?
"""
stmt = session.prepare(DELETE_MOVIE_TITLE)
session.execute(stmt, ("Greatest Hits", 2022, "Song_1"))

DELETE_MOVIE_GENRE = """
DELETE FROM movies_by_genre
WHERE genre =? AND title = ?
    AND = release_year = ?
"""
smt = sessio.prepare(DELETE_MOVIE_GENRE)

# ELIMINAR TABLA Y CERRAR CONEXION
DROP_TABLE = "DROP TABLE IF EXISTS spotify_songs"
stmt = session.prepare(DROP_TABLE)
session.execute(stmt)

Cluster.shutdown()
