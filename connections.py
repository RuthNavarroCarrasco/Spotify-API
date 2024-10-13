import os, sys
import urllib
import pyodbc
from sqlalchemy import create_engine, text


DRIVER = "{ODBC Driver 18 for SQL Server}"
AZURE_SERVER = os.getenv("AZURE_SERVER")
DATABASE = os.getenv("DATABASE")
AZURE_USER = os.getenv("AZURE_USER")
AZURE_PASSWORD = os.getenv("AZURE_PASSWORD")

#connection_string = f"Driver={DRIVER};Server=tcp:myspotifywrap.database.windows.net,1433;Database=Wrapped;Uid={UID};Pwd={PWD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


# "jdbc:sqlserver://;serverName=myspotifywrap.database.windows.net;databaseName=Wrapped;encrypt=true"
# with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+AZURE_SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+UID+';PWD='+ PWD) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
#         row = cursor.fetchone()
#         while row:
#             print (str(row[0]) + " " + str(row[1]))
#             row = cursor.fetchone()

conn = pyodbc.connect(f"Driver={DRIVER};Server=tcp:{AZURE_SERVER},1433;Database={DATABASE};Uid={AZURE_USER};Pwd={AZURE_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

print(conn)

cursor = conn.cursor()
cursor.execute("SELECT * from artists")
dataset = cursor.fetchall()
print(dataset)