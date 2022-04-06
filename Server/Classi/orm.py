import psycopg2
import json
import time
from .peer import Peer
from .log import Log
from enum import Enum

class ORM:
    
    #costruttore
    def __init__(self):
        try:
            
            #lettura file json di configurazione server db
            filename = "Classi/config.json"
            with open(filename, "r") as dictionary:
                configDict = json.load(dictionary)

            #connessione al server
            self.connection = psycopg2.connect(
                database = configDict["DB_NAME"], 
                user = configDict["USER"], 
                password = configDict["PSW"], 
                host = configDict["IP"], 
                port = configDict["PORT"]
                )
            
            self.connection.autocommit = True
        except Exception as ex:
            print(ex.__str__())

    #region PEER

    def addPeer(self, peer):
        query = "INSERT INTO peer (session_id, ip_peer, port_peer) VALUES ('%s', '%s', '%s')" %(peer.get_session_id(), peer.get_ip(), peer.get_port())
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Peer aggiunto correttamente")
            l = Log(peer.get_session_id(), Tipo_Operazione.Login, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            self.addLog(l)
        except Exception as ex:
            print(ex.__str__())

    def selectPeer(self, ip, port):
        query = "SELECT * FROM peer WHERE ip_peer = %s AND port_peer = %s" %(ip, port)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            #cursor.fetchall()
        except Exception as ex:
            print(ex.__str__())

    def checkPeer(self, sessionID):
        query = "SELECT * FROM peer WHERE session_id = %s" %sessionID
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            #cursor.fetchall()
        except Exception as ex:
            print(ex.__str__())

    def deletePeer(self, sessionID):
        query = "DELETE FROM peer WHERE session_id = %s" %sessionID
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Peer rimosso correttamente")
            l = Log(sessionID, Tipo_Operazione.Logout, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            ORM.addLog(l)
        except Exception as ex:
            print(ex.__str__())

    #endregion

    #region LOG
    def addLog(self, log):
        query = "INSERT INTO log (session_id, data, ora, operazione) VALUES('%s', '%s', '%s', '%s')" %(log.sessionID, log.data, log.ora, log.tipo_operazione.__str__())
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Log creato")
        except Exception as ex:
            print(ex.__str__())

    def selectLog(self, sessionID):
        query = "SELECT * FROM log WHERE session_id = %s" %sessionID
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    #endregion

    #region FILE
    def addFile(self, md5_File, filename, filepath):
        query = "INSERT INTO file (*) VALUES(%s, %s, %s)" %(md5_File, filename, filepath)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def selectfile(self, filename):
        query = "SELECT * FROM file WHERE filename = %s" %filename
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def updateFile(self, newFilename, newFilepath, md5_File):
        query = "UPDATE file SET filename = %s, filepath = %s WHERE md5_file = %s" %(newFilename, newFilepath, md5_File)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())
    
    def deleteFile(self, md5_file):
        query = "DELETE FROM file WHERE md5_file = %s" %md5_file
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    #endregion

    #region PEER_FILE
    def selectPeerFile(self, sessionID, md5_file):
        query = "SELECT * FROM peer_file WHERE session_id = %s AND md5_file = %s" %(sessionID, md5_file)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def addPeerFile(self, sessionID, md5_file, copia):
        query = "INSERT INTO peer_file (*) VALUES(%s, %s, %d)" %(sessionID, md5_file, copia)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())
    
    #endregion

#enumeratore tipo di operazione per log
class Tipo_Operazione(Enum):
    Login = 1,
    Logout = 2,
    AddFile = 3,
    DeleteFile = 4,
    SearchFile = 5,
    DownloadFile = 6,
    SearchPeer = 7,