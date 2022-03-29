import psycopg2

try: 
    connessione = psycopg2.connect(database = "postgres",
        user = 'postgres',
        password = 'password',
        host = 'localhost',
        port = '5432'
    ) 
    #database = "<nomeDB>" user = '<username>' password = '<password>' host = '<localhost>' port = '<5432>'
    connessione.autocommit = True

    cursor = connessione.cursor()
    nomeDB = "Prova"

    sqlQuery = "create database %s " %nomeDB
    cursor.execute(sqlQuery)
    print("Database creato con successo")
except Exception as ex:
    print("Errore!")