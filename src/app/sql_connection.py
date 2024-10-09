import os
import urllib
import pyodbc
from sqlalchemy import create_engine, text, inspect


DRIVER = "ODBC Driver 18 for SQL Server"
AZURE_SERVER = os.getenv("AZURE_SERVER")
DATABASE = os.getenv("DATABASE")
UID = os.getenv("UID")
PWD = os.getenv("PWD")

params = urllib.parse.quote_plus(
    'Driver={{ODBC Driver 18 for SQL Server}};'
    f'Server=tcp:{AZURE_SERVER},1433;'
    f'Database={DATABASE};'
    f'Uid={UID};'
    f'Pwd={PWD};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)

# Crear el engine utilizando SQLAlchemy
conn_str = f'mssql+pyodbc:///?odbc_connect={params}'
engine_azure = create_engine(conn_str, echo=True)

# Probar la conexión y listar las tablas en la base de datos
print('Connection is ok')
inspector = inspect(engine_azure)
tables = inspector.get_table_names()

# Imprimir la lista de nombres de tablas
print('Connection is ok')
print('Tables in the database:', tables)

# def create_connection():
#     """
#     Crea una conexión a la base de datos utilizando SQLAlchemy y devuelve el engine.
#     """
#     try:
#         # Crea la cadena de conexión usando SQLAlchemy
#         engine = create_engine(
#             f"mssql+pyodbc://{UID}:{PWD}@{AZURE_SERVER}/{DATABASE}?driver={DRIVER}&Trusted_Connection=no&Encrypt=yes"
#         )
#         print("Conexión exitosa")
#         print(engine)
#         return engine

#     except Exception as ex:
#         print(f"Error al conectar con la base de datos: {ex}")
#         return None


# def insert(engine, insert_query, verification_query):
#     """
#     Verifica si los datos ya existen en la base de datos antes de insertar.
    
#     :param engine: El engine de la conexión a la base de datos.
#     :param insert_query: La consulta SQL para insertar los datos.
#     :param verification_query: La consulta SQL para verificar si los datos ya existen.
#     """
#     try:
#         with engine.connect() as connection:
#             # Primero, ejecuta la consulta de verificación
#             result = connection.execute(text(verification_query))
#             verification_result = result.fetchall()
#             print("query de verificacion hecha")
#             if verification_result:
#                 print("El registro ya existe en la base de datos. No se realizará la inserción.")
#             else:
#                 # Si no existe, ejecuta la consulta de inserción
#                 connection.execute(text(insert_query))
#                 print("Inserción realizada con éxito.")

#     except Exception as ex:
#         print(f"Error al verificar e insertar los datos: {ex}")

