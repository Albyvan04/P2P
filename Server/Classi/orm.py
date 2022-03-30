from multiprocessing import connection
import psycopg2
import peer

DB_NAME = "ProvaDB"
USERNAME = ""
PASSWORD = ""
SERVER_PORT = "80"

class ORM:
    
    def __init__(self, ip):
        try:
            connection = psycopg2.connect(database = DB_NAME, user = USERNAME, password = PASSWORD, host = ip, port = SERVER_PORT)
            connection.autocommit = True
        except Exception as ex:
            print(ex.__str__())

    def selectPeer(ip, port):
        query = "SELECT * FROM PEER WHERE IP_PEER = %s AND PORT_PEER = %s" %(ip, port)
        cursor = connection.cursor()
        cursor.execute(query)



