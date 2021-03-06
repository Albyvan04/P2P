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
        query = "INSERT INTO peer (session_id, ip_peer, port_peer) VALUES ('%s', '%s', '%s')" %(peer.session_id, peer.ip, peer.port)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Peer aggiunto correttamente")
        except Exception as ex:
            print("Aaaaa")
            print(ex.__str__())

    def selectPPeer(self, ip, port):
        query = "SELECT * FROM peer WHERE ip_peer = '%s' AND port_peer = %d" %(ip, int(port))
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            peer = cursor.fetchone()
            peer = Peer(peer[0], peer[1], peer[2])
            return peer
        except Exception as ex:
            print(ex.__str__())

    def selectPeer(self, sessionID):
        query = "SELECT * FROM peer WHERE session_id = '%s'" %(sessionID)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchone()
        except Exception as ex:
            print(ex.__str__())

    def checkPeer(self, sessionID):
        query = "SELECT * FROM peer WHERE session_id = %s" %sessionID
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as ex:
            print(ex.__str__())

    def deletePeer(self, sessionID):
        query = "DELETE FROM peer WHERE session_id = '%s'" %sessionID
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Peer rimosso correttamente")
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
        query = "SELECT * FROM log WHERE session_id = '%s'" %sessionID
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    #endregion

    #region FILE
    def addFile(self, md5_File, sessionId, filename, copia):
        query = "INSERT INTO file (md5_file, filename, session_id, copia) VALUES('%s', '%s', '%s', %s)" %(md5_File, filename, sessionId, copia)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def selectfile(self, filename):
        query = "SELECT * FROM file WHERE filename LIKE '%" + filename + "%'"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            lista = cursor.fetchall()

            if(len(lista) != 0):
                return lista, True
            else:
                return lista, False
        except Exception as ex:
            print(ex.__str__())
        print("bbbbbb")
        return None, False

    def selectIDfile(self, sessionID, md5_file):
        query = "SELECT id FROM file WHERE session_id = '%s' and md5_file = '%s'" %(sessionID, md5_file)
        cursor = self.connection.cursor()
        #try:
        cursor.execute(query)
        return cursor.fetchone()
     
        #except Exception as ex:
            #print(ex.__str__())
    
    def deleteFile(self, sessionId, md5_file):
        query = "DELETE FROM file WHERE session_id = '%s' AND md5_file = '%s'" %(sessionId, md5_file)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return True
        except Exception as ex:
            print(ex.__str__())
        return False

    def deleteAllFile(self, sessionID):
        query = "DELETE FROM file WHERE session_id = '%s'" %sessionID
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return 1
        except Exception as ex:
            print(ex.__str__())
        return -1

    def selectPeerFile(self, sessionID):
        query = "SELECT * FROM file WHERE session_id = '%s'" %(sessionID)
        cursor = self.connection.cursor()
        try:    
            cursor.execute(query)

            md5list = []
            for el in cursor.fetchall():
                md5list.append(el["md5_file"])
            
            return md5list
        except Exception as ex:
            print(ex.__str__())

    def selectCopyFile(self, md5_file):
        query = "SELECT MAX(copia) FROM file WHERE md5_file = '%s'" %md5_file
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchone()[0] or -1
               
        except Exception as ex:
            print(ex.__str__())
            return -1

    def countFile(self, sessionId):
        query = "SELECT COUNT(*) FROM file WHERE session_id = '%s'" %sessionId
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            nFile = cursor.fetchone()
            return nFile[0]
        except Exception as ex:
            print(ex.__str__())
    
    #endregion

    #region DOWNLOAD
    def addDownload(self, sessionId, id_file):
        query = "INSERT INTO download (session_id, id_file) VALUES('%s', '%d')" %(sessionId, id_file)
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Download registrato nel database")
        except Exception as ex:
            print("orm", ex.__str__())

    def countDownload(self, id_file):
        query = "SELECT COUNT(*) FROM download WHERE id_file = '%s'" %id_file
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchone()[0]
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

