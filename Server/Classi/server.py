import socket
import time
from .peer import Peer
from .orm import ORM, Tipo_Operazione
from .log import Log
from .utilitiesServer import Utilities


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
            l = Log(peer.get_session_id(), Tipo_Operazione.Login, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            ORM.addLog(l)
            return peer, True

        except Exception as ex:
            print(ex.__str__())

        return peer, False

    @staticmethod
    def addFile(request):

        session_id = request[4:20]
        md5_file = request[20:52]
        filename = request[52:152]

        orm = ORM()

        try:
            orm.addFile(md5_file, filename)
            nCopia = orm.selectCopyFile(md5_file) + 1
            orm.addPeerFile(session_id, md5_file, nCopia)
            l = Log(session_id, Tipo_Operazione.AddFile, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            ORM.addLog(l)
            return nCopia, True
        except Exception as ex:
            print(ex.__str__())
        return -1, False
            
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
        orm = ORM()

        try:
            
            #conto il numero di file associati a quel peer per restituirlo in risposta
            nFile = orm.countFile(sessionId)

            #prelevo gli md5 dei file di quel peer per eliminarli
            md5list = orm.selectPeerFile(sessionId)

            #elimino ogni file 
            for md in md5list:
                orm.deleteFile(md, )
            
            #elimino il peer dalla lista
            orm.deletePeer(sessionId)

            return True
        except Exception as ex:
            print(ex.__str__())
        return False
