from cassandra.cluster import Cluster
import uuid

#
CREATE_KEYSPACE = """
    CREATE KEYSPACE IF NOT EXISTS movies
    WITH replication = { 'class': 'SimpleStrategy','replication_factor':1}
   """

CREATE_TABLE_MOVIE_BY_TITLE = """
    CREATE TABLE IF NOT EXISTS movies_by_title (movie_id UUID, title TEXT, release_year INT, genre TEXT, rating FLOAT, director TEXT,
        PRIMARY KEY (title, release_year)
)
"""
CREATE_TABLE_MOVIE_BY_GENRE = """
    CREATE TABLE IF NOT EXISTS movies_by_genre (movie_id UUID, title TEXT, release_year INT, genre TEXT, rating FLOAT, director TEXT,
        PRIMARY KEY ((genre), rating)

)
"""
INSERT_MOVIE_TITLE = """ 
        INSERT INTO movies_by_title(movie_id, title, release_year, genre, rating, director)
        VALUES (?, ?, ?, ?, ?, ?)
"""        
INERT_MOVIES_GENRE = """
    INSERT INTO movies_by_genre(movie_id, title, release_year, genre, rating, director)
    VALUES (?, ?, ?, ?, ?, ?)
"""
    
SELECT_BY_TITLE = """
    SELECT * FROM movies_by_title WHERE title = ? AND release_year = ?
"""
     
SELECT_BY_GENRE = """
    SELECT * FROM movies_by_genre WHERE genre = ? ORDER BY rating DESC
"""
         

UPDATE_MOVIE_DIRECTOR_T = """
    UPDATE movies_by_title SET director=? WHERE title=? AND release_year=? 
"""
UPDATE_MOVIE_DIRECTOR_G = """
    UPDATE movies_by_genre SET director=? WHERE genre=? AND rating=? 
"""

DELETE_MOVIE_TITLE = """
    DELETE FROM movies_by_title WHERE title =? AND release_year = ?
"""

DELETE_MOVIE_GENRE = """
    DELETE FROM movies_by_genre WHERE genre =? AND rating = ?
"""

def create_keyspace_and_tables(session):
    # Crearr keyspace
    session.execute(CREATE_KEYSPACE)
    session.set_keyspace("movies")
    print("Creacion de keyspace exitoso")
    # CREACION DE TABLAS
    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_TITLE)
    session.execute(stmt)
    print("Tabla creada: movies_by_title")

    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_GENRE)
    session.execute(stmt)
    print("Tabla creada: movies_by_genre")
pass

# INSERTS ------------------------------------------------------------------------
def insert_movie(session, title, year, director, genre, rating): 
    movie_id = uuid.uuid4()
    stmt = session.prepare(INSERT_MOVIE_TITLE)   
    session.execute(stmt, (movie_id, title, year, genre, rating, director))

    stmt = session.prepare(INERT_MOVIES_GENRE)   
    session.execute(stmt, (movie_id, title, year, genre, rating, director))
    pass
# ----------------------------------------------------------------------------------------
# CONSULTAR DATOS
# por titulo

def query_by_title(session, title, year):
    stmt = session.prepare(SELECT_BY_TITLE)
    rows = session.execute(stmt, (title, year))
    print('>>\n')
    for r in rows:
        print(f'Título: {r.title}\nAño de estreno: {r.release_year}\n')
    pass

def query_by_genre(session, genre):
# consylta por genero
    stmt = session.prepare(SELECT_BY_GENRE)
    rows = session.execute(stmt, (genre,))
    print(f'Género:{genre}\n')
    for r in rows:
        print(f'Titulo: {r.title} - Rating: {r.rating}\n')
    pass

# ----------------------------------------------------------------------------------------
# ACTUALIZAR DATAZOAOS
def update_movie_director(session, title, release_year, genre, rating, new_director):   
    stmt = session.prepare(UPDATE_MOVIE_DIRECTOR_T)
    session.execute(stmt, (new_director, title, release_year))
    stmt = session.prepare(UPDATE_MOVIE_DIRECTOR_G)
    session.execute(stmt, (new_director, genre, rating))
    pass

def delete_movie(session, title, release_year, genre, rating):
# ELIMINAR DATOS
    stmt = session.prepare(DELETE_MOVIE_TITLE)
    session.execute(stmt, (title, release_year ))
    
    stmt = session.prepare(DELETE_MOVIE_GENRE)
    session.execute(stmt, (genre, rating))
        
    pass

# --------------------------------------

def main():
#    cluster = Cluster(['127.0.0.1'])
    cluster = Cluster(['172.26.160.1'], port=9024)  #PARA QUE RODRIGO LE FUNCIONE TIENE QUE PONER ESTO
                                                    #EN CASO DE NO ESTAR SALADO COMO RODRIGO NO ES NECESARIO (CREO)

    session = cluster.connect()
    create_keyspace_and_tables(session)

    while True:
        print("\n=== Movie Database Menu ===")
        print("1. Insertar película")
        print("2. Consultar por título")
        print("3. Consultar por género")
        print("4. Actualizar director")
        print("5. Eliminar película")
        print("0. Salir")
        choice = input("Seleccione opción: ")
        
        if choice == "1":
            title = input("Título: ")
            year = int(input("Año: "))
            director = input("Director: ")
            genre = input("Género: ")
            rating = float(input("Rating: "))
            insert_movie(session, title, year, director, genre, rating)
        elif choice == "2":
            title = input("Título: ")
            year = int(input("Año: "))
            query_by_title(session, title, year)
        elif choice == "3":
            genre = input("Género: ")
            query_by_genre(session, genre)
        elif choice == "4":
            title = input("Título: ")
            release_year = int(input("Año:"))
            new_director = input("Nuevo Director: ")
            genre = input("Género: ")
            rating = float(input("Rating: "))

            update_movie_director(session, title, release_year, genre,rating, new_director)
        elif choice == "5":
            # Eliminar de movie_by_title -> title, release_year
            # Eliminar de movie_by_genre -> genre, rating
            title = input("Título: ")
            genre = input("Género: ")
            rating = float(input("Rating: "))
            release_year = int(input("Año: "))
            delete_movie(session, title, release_year, genre, rating)
        elif choice == '0':
        # Cerrar conexión y salir
            cluster.shutdown()
            break;
            pass
        else:
            print("Opción inválida") 
            break

if __name__ == "__main__":
    main()