import psycopg2

try: 
    connessione = psycopg2.connect(database = "postgres",
        user = 'postgres',
        password = 'password',
        host = 'localhost',
        port = '5432'
    ) 
    #esempio connessione al DB ===> database = "<nomeDB>" user = '<username>' password = '<password>' host = '<localhost>' port = '<5432>'
    connessione.autocommit = True
    cursor = connessione.cursor()
    #creazione DB
    nomeDB = "Prova"
    sqlQuery = "create database %s " %nomeDB
    cursor.execute(sqlQuery)
    print("Database creato con successo")
    #tabella peer
    tabellaPeer = "create table PEER(SESSION_ID varchar(50) PRIMARY KEY, IP_PEER VARCHAR(15) NOT NULL UNIQUE, PORT_PEER INTEGER NOT NULL);"
    cursor.execute(tabellaPeer)
    print("Tabella Peer creata con successo")
    #tabella log
    tabellaLog = "CREATE TABLE LOG(ID INTEGER PRIMARY KEY,SESSION_ID VARCHAR(50) REFERENCES PEER(SESSION_ID) NOT NULL,DATA DATE NOT NULL,ORA TIME NOT NULL,OPERAZIONE VARCHAR(50) NOT NULL);"
    cursor.execute(tabellaLog)
    print("Tabella Log creata con successo")
    #tabella file
    tabellaFile = "CREATE TABLE FILE(MD5_FILE VARCHAR(50) PRIMARY KEY,FILENAME VARCHAR(50) NOT NULL,FILEPATH VARCHAR(100) NOT NULL);"
    cursor.execute(tabellaFile)
    print("Tabella File creata con successo")
    #tabella peer_file
    tabellaPeer_File = "CREATE TABLE FILE_PEER(SESSION_ID VARCHAR(50) REFERENCES PEER(SESSION_ID) NOT NULL,MD5_FILE VARCHAR(50) REFERENCES FILE(MD5_FILE) NOT NULL,COPIA INTEGER NOT NULL);"
    cursor.execute(tabellaPeer_File)
    print("Tabella Peer_File creata con successo")
    #tabella download
    tabellaDownload = "CREATE TABLE DOWNLOAD(SESSION_ID VARCHAR(50) REFERENCES PEER(SESSION_ID) NOT NULL,MD5_FILE VARCHAR(50) REFERENCES FILE(MD5_FILE) NOT NULL);"
    cursor.execute(tabellaDownload)
    print("Tabella Download creata con successo")
except Exception as ex:
    print("Errore!")