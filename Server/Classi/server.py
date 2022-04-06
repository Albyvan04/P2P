import socket
from peer import Peer
from orm import ORM
from utilitiesServer import Utilities


class Server:

    @staticmethod
    def login(request):

        #parsing pacchetto
        ipClient = request[4:19]
        portClient = request[19:24]

        #generazione session id random
        sessionId = Utilities.generateSessionID()

        peer = Peer(sessionId, ipClient, portClient)
        orm = ORM()

        try:

            #nuovo peer su db
            orm.addPeer(peer)
            return peer, True

        except Exception as ex:
            print(ex.__str__())

        return peer, False

    @staticmethod
    def addFile(socket):
        #aggiungere in database
        socket.send(("AADD").encode()) #manca attributo

    @staticmethod
    def removeFile(socket, sessionId):
        return ""
    
    @staticmethod
    def searchFile(socket, sessionId):
        return ""

    @staticmethod
    def download(socket, sessionId):
        return ""

    @staticmethod
    def logout(request):
        sessionId = request[4:20]
        try:
            ORM.deletePeer(sessionId)
            #finire il pacchetto
            return True
        except Exception as ex:
            print(ex.__str__())
        return False
