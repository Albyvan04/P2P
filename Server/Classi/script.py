import psycopg2
import json

try: 

    #lettura file json di configurazione server db
    filename = "Classi/config.json"
    with open(filename, "r") as dictionary:
        configDict = json.load(dictionary)

    #lettura file json di query creazione db
    filename = "Classi/query.json"
    with open(filename, "r") as dictionary:
        queryDict = json.load(dictionary)

    #connessione al server db
    connessione = psycopg2.connect(
        database = configDict["DEFAULT_DB_NAME"],
        user = configDict["USER"],
        password = configDict["PSW"],
        host = configDict["IP"],
        port = configDict["PORT"]
    ) 
    #esempio connessione al DB ===> database = "<nomeDB>" user = '<username>' password = '<password>' host = '<localhost>' port = '<5432>'

    #crea in automatico la connessione e rimane aperta
    connessione.autocommit = True

    #creo l'oggetto per lanciare le query
    cursor = connessione.cursor()

    #creazione DB
    dropDb = queryDict["DROPDB"]
    cursor.execute(dropDb)
    createDb = queryDict["CREATEDB"]
    cursor.execute(createDb)
    print("Database creato con successo")

    #ricreo la connessione sul DB appena creato
    connessione = psycopg2.connect(
        database = configDict["DB_NAME"],
        user = configDict["USER"],
        password = configDict["PSW"],
        host = configDict["IP"],
        port = configDict["PORT"]
    ) 

    connessione.autocommit = True
    cursor = connessione.cursor()

    #tabella peer
    tabellaPeer = queryDict["CREATETAB_PEER"]
    cursor.execute(tabellaPeer)
    print("Tabella Peer")   

    #tabella log
    tabellaLog = queryDict["CREATETAB_LOG"]
    cursor.execute(tabellaLog)
    print("Tabella Log")

    #tabella file
    tabellaFile = queryDict["CREATETAB_FILE"]
    cursor.execute(tabellaFile)
    print("Tabella File")

    #tabella download
    tabellaDownload = queryDict["CREATETAB_DOWNLOAD"]
    cursor.execute(tabellaDownload)
    print("Tabella Download")

except Exception as ex:
    print("%s" %ex)


##########################
# CREAZIONE FILE JSON DB #
##########################
#filename = "query.json"

#jsonObject = {
    #    "DROPDB": "DROP DATABASE IF EXISTS %s" %DB_NAME,
    #    "CREATEDB": "CREATE DATABASE %s" %DB_NAME,
    #    "CREATETAB_PEER": "CREATE TABLE IF NOT EXISTS peer (session_id varchar(50) PRIMARY KEY, ip_peer VARCHAR(15) NOT NULL UNIQUE, port_peer INTEGER NOT NULL);",
    #    "CREATETAB_LOG": "CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, session_id VARCHAR(50) REFERENCES peer(session_id) NOT NULL, data DATE NOT NULL, ora TIME NOT NULL, operazione VARCHAR(50) NOT NULL);",
    #    "CREATETAB_FILE": "CREATE TABLE IF NOT EXISTS file (md5_file VARCHAR(50) PRIMARY KEY, filename VARCHAR(50) NOT NULL, filepath VARCHAR(100) NOT NULL);",
    #    "CREATETAB_FILE_PEER": "CREATE TABLE IF NOT EXISTS file_peer (session_id VARCHAR(50) REFERENCES peer(session_id) NOT NULL, md5_file VARCHAR(50) REFERENCES file(md5_file) NOT NULL, copia INTEGER NOT NULL);",
    #    "CREATETAB_DOWNLOAD": "CREATE TABLE IF NOT EXISTS download (session_id VARCHAR(50) REFERENCES peer(session_id) NOT NULL, md5_file VARCHAR(50) REFERENCES file(md5_file) NOT NULL);",
    #}
    #with open(filename, "w") as output:
    #    json.dump(jsonObject, output)


######################################
# CREAZIONE FILE JSON CONFIGURAZIONE #
######################################
#filename = "config.json"
#
#jsonObject = {
#        "DEFAULT_DB_NAME": "postgres",
#        "DB_NAME": "napster",
#        "USER": "postgres",
#        "PSW": "password",
#        "IP": "localhost",
#        "PORT": "5432"
#    }
#
#with open(filename, "w") as output:
#    json.dump(jsonObject, output)