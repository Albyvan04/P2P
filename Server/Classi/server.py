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

            #creo il log
            l = Log(peer.get_session_id(), Tipo_Operazione.Login, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            orm.addLog(l)
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

            #mi prelevo l'ultima copia aggiunta
            nCopia = orm.selectCopyFile(md5_file) + 1

            #aggiungo il file
            orm.addFile(md5_file, session_id, filename, nCopia)

            #creo il log
            l = Log(session_id, Tipo_Operazione.AddFile, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            orm.addLog(l)

            #ritorno il numero di copia aggiunto per il pacchetto di risposta
            return nCopia, True

        except Exception as ex:
            print(ex.__str__())
        return -1, False
            
    @staticmethod
    def removeFile(request):

        sessionId = request[4:20]
        md5_file = request[20:52]

        orm = ORM()

        try:
            nFile = orm.deleteFile(sessionId, md5_file)

            if(nFile > 0):
                nCopie = orm.selectCopyFile(md5_file)
                return nCopie, True

            return -1, False

        except Exception as ex:
            print(ex.__str__())
        
        return False

    
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

            #elimino i file di quel peer
            orm.deleteFile(sessionId)
            
            #elimino il peer dalla lista
            orm.deletePeer(sessionId)

            #creo il log
            l = Log(sessionId, Tipo_Operazione.Logout, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            orm.addLog(l)

            return True
        except Exception as ex:
            print(ex.__str__())
        return False
