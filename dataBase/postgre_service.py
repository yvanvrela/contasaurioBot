import os
import psycopg2
from psycopg2 import Error


def conection_db():
    """
        Crea la conexión a la base de datos con
        Postgresql.
        :return Connection object or None
    """

    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn = psycopg2.connect(
        host="localhost",
        database="contribuyentes_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

    return conn


def create_table() -> None:
    """ Crea la tabla en la base de datos,
        si aún no existe. Indicando la base de datos
        especifica.
        :return None
    """
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS contribuyentes (
                id	 INT PRIMARY KEY NOT NULL,
                fullname	VARCHAR(255) UNIQUE NOT NULL,
                dv VARCHAR(10) NOT NULL,
                ruc VARCHAR(255) NOT NULL
            );""")
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def put_contribuyente(data: dict) -> None:
    try:
        conn = conection_db()
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO contribuyentes (id, fullname, dv, ruc)\
                VALUES('{data['ci']}', '{data['fullname']}', '{data['dv']}', '{data['ruc']}')")

        conn.commit()
    except Error as e:
        conn.close()
        print(e)


def delete_contribuyente(id_contribuyente) -> None:
    conn = conection_db()
    try:
        cursor = conn.cursor()

        cursor.execute(
            f"DELETE FROM contribuyentes WHERE id = {id_contribuyente}")

        conn.commit()
        conn.close()
    except Error as e:
        conn.close()
        print(e)
