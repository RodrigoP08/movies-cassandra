from cassandra.cluster import Cluster
import uuid

# conectarse al cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
print('Se conecto bien a cassandra')

# Crearr keyspace
CREATE_KEYSPACE = """
CREATE KEYSPACE IF NOT EXISTS movies
WITH replication = { 'class':
                    'SimpleStrategy','replication_factor':1}
"""
session.execute(CREATE_KEYSPACE)
session.set_keyspace("spotify")


# CREACION DE TABLAS
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS movies_by_title (movie_id UUID, title TEXT, release_year INT, genre TEXT, rating FLOAT, director TEXT,
                                          PRIMARY KEY ((title), release_year)
)
"""
stmt = session.prepare(CREATE_TABLE)
session.execute(stmt)
print("Tabla creada: movies_by_title")


CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS movies_by_genre (movie_id UUID, title TEXT, release_year INT, genre TEXT, rating FLOAT, director TEXT,
                                          PRIMARY KEY ((genre), rating)
)
"""
stmt = session.prepare(CREATE_TABLE)
session.execute(stmt)
print("Tabla creada: movies_by_genre")

# INSERTS ------------------------------------------------------------------------
INSERT_MOVIES = """
INSERT INTO movies_by_title(movie_id, title, release_year, genre, rating, director)
VALUES (?, ?, ?, ?, ?, ?)
"""
movie_id = uuid.uuid4()
stmt = session.prepare(INSERT_MOVIES)   
session.execute(stmt, (movie_id, "Malefica", 2014, "Ciencia fixion", 5, "cynthia"))


INERT_MOVIES = """
INSERT INTO movies_by_genre(movie_id, title, release_year, genre, rating, director)
VALUES (?, ?, ?, ?, ?, ?)
"""
movie_id = uuid.uuid4()
stmt = session.prepare(INSERT_MOVIES)   
session.execute(stmt, (movie_id, "Malefica", 2014, "Ciencia fixion", 5, "cynthia"))
# ----------------------------------------------------------------------------------------
# CONSULTAR DATOS
# por titulo
SELECT_ALL = "SELECT * FROM movies_by_title"
stmt = session.prepare(SELECT_ALL)
rows = session.execute(stmt)

for r in rows:
    print(r.title, r.release_year, r.genre, r.rating, r.dierctor)

# consylta por genero
SELECT_ALL = "SELECT * FROM movies_by_genre"


# ----------------------------------------------------------------------------------------
# ACTUALIZAR DATAZOAOS
UPDATE_RATING = """
UPDATE movies_by_genre
SET rating=?
WHERE title=? AND release_year=?
    AND dierctor=?
"""
stmt = session.prepare(UPDATE_RATING)
session.execute(stmt, (5.0, "Greatest Hits", 2022, "Song_1"))

# ELIMINAR DATOS
DELETE_BY_RATING = """
DELETE FROM spotify_songs
WHERE album=? AND release_year=?
    AND song_name=?
"""
stmt = session.prepare(DELETE_BY_RATING)
session.execute(stmt, ("Greatest Hits", 2022, "Song_1"))

# ELIMINAR TABLA Y CERRAR CONEXION
DROP_TABLE = "DROP TABLE IF EXISTS spotify_songs"
stmt = session.prepare(DROP_TABLE)
session.execute(stmt)

Cluster.shutdown()
