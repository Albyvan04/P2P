import psycopg2
import peer

DB_NAME = "ProvaDB"
USERNAME = "albyvan04"
PASSWORD = "admin"
SERVER_PORT = "5432"

class ORM:
    
    def __init__(self, ip):
        try:
            connection = psycopg2.connect(database = DB_NAME, user = USERNAME, password = PASSWORD, host = ip, port = SERVER_PORT)
            connection.autocommit = True
        except Exception as ex:
            print(ex.__str__())

    #def selectPeer(ip, port):
    #    query = "SELECT * FROM PEER WHERE IP_PEER = %s AND PORT_PEER = %s" %(ip, port)
    #    cursor = connection.cursor()
    #    cursor.execute(query)
    #    user = cursor.fetchall()
    #    peer = Peer(user[0]["SESSION_ID"], user[1]["IP_PEER"], )

orm = ORM("25.72.89.220")

