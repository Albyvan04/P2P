import psycopg2
import json
import peer

class ORM:
    
    def __init__(self, ip):
        try:

            filename = "config.json"
            with open(filename, "r") as dictionary:
                configDict = json.load(dictionary)

            connection = psycopg2.connect(
                database = configDict["DB_NAME"], 
                user = configDict["USER"], 
                password = configDict["PSW"], 
                host = configDict["IP"], 
                port = configDict["PORT"]
                )
            
            connection.autocommit = True
        except Exception as ex:
            print(ex.__str__())

    #peer
    def selectPeer(ip, port):
        query = "SELECT * FROM PEER WHERE IP_PEER = %s AND PORT_PEER = %s" %(ip, port)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            #cursor.fetchall()
        except Exception as ex:
            print(ex.__str__())

    def checkPeer(sessionID):
        query = "SELECT * FROM PEER WHERE SESSION_ID = %s" %sessionID
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            #cursor.fetchall()
        except Exception as ex:
            print(ex.__str__())

    def deletePeer(sessionID):
        query = "DELETE FROM PEER WHERE SESSION_ID = %s" %sessionID
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    #log
    def addLog(ID, sessionID, tipo_operazione, data, ora):
        query = "INSERT INTO LOG VALUES(%s, %s, %s, %s, %s)" %(ID, sessionID, tipo_operazione, data, ora)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def selectLog(sessionID):
        query = "SELECT * FROM LOG WHERE SESSION_ID = %s" %sessionID
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    #file
    def addFile(md5_File, filename, filepath):
        query = "INSERT INTO FILE VALUES(%s, %s, %s)" %(md5_File, filename, filepath)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def selectfile(filename):
        query = "SELECT * FROM FILE WHERE FILENAME = %s" %filename
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def updateFile(newFilename, newFilepath, md5_File):
        query = "UPDATE SET FILENAME = %s, FILEPATH = %s WHERE MD5_FILE = %s" %(newFilename, newFilepath, md5_File)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())
    
    def deleteFile(md5_file):
        query = "DELETE FROM FILE WHERE MD5_FILE = %s" %md5_file
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    #peer_file
    def selectPeerFile(sessionID, md5_file):
        query = "SELECT * FROM PEER_FILE WHERE SESSION_ID = %s AND MD5_FILE = %s" %(sessionID, md5_file)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())

    def addPeerFile(sessionID, md5_file, copia):
        query = "INSERT INTO PEER_FILE VALUES(%s, %s, %d)" %(sessionID, md5_file, copia)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex.__str__())
    