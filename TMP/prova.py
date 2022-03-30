from msilib.schema import File
from multiprocessing import connection
from file import File
from log import Log
import psycopg2

connessione = psycopg2.connect(database = "postgres",
        user = 'postgres',
        password = 'password',
        host = 'localhost',
        port = '5432'
    ) 

def addFile(nomefile, percorsoFile):
    f = File(nomefile, percorsoFile)
    md5_file = f.get_md5()
    query = "INSERT INTO FILE(MD5_FILE, FILENAME, FILEPATH) VALUES(%s, %s, %s)" %(md5_file, nomefile, percorsoFile)
    connessione.autocommit = True
    cursor = connessione.cursor()
    cursor.execute(query)
