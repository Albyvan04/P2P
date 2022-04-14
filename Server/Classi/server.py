from pickle import TRUE
import socket
import time
from .peer import Peer
from .orm import ORM, Tipo_Operazione
from .log import Log
from .utilitiesServer import Utilities
from .file import File


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
            l = Log(peer.session_id, Tipo_Operazione.Login, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
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
    def searchFile(request):
        sessionId = request[4:20]
        ricercato = (request[20:40].decode()).strip()

        orm = ORM()

        try:
            filesTmp = orm.selectfile(ricercato)
            files = []

            for index, file in filesTmp:

                isNewMD5 = True
                indexOldMD5 = 0

                for i, el  in files:
                    if file[1] == el.MD5 :
                        isNewMD5 = False
                        indexOldMD5 = i

        
                if(isNewMD5):
                    files.append(File(file[3], file[1]))

                peer = orm.selectPeer(file[2])

                if(isNewMD5):
                    files[index].addPeer(Peer(peer[0], peer[1], peer[2]))
                else:
                    files[indexOldMD5].addPeer(Peer(peer[0], peer[1], peer[2]))

            if(files.count() == 0):
                return 0
            else:

                request = "AFIN" + str(len(files)) 

                for file in files:

                    # print("ID = %s\t\t", row[0])
                    # print("Filename = %s\t\t", row[3])
                    # print("MD5 = %s\t\t", row[1])
                    # print("SessionId = %s\t\t", row[2])
                    # print("Copia = %s\t\t", row[4])

                    request += file.MD5 + file.fileName + len(file.peers)

                    for peer in file.peers:
                        request += peer.ip + peer.port
                
                return 1

        except Exception as ex:
            print(ex.__str__())

         
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
            nDelete = orm.deleteFile(sessionId)
            
            #elimino il peer dalla lista
            orm.deletePeer(sessionId)

            #creo il log
            l = Log(sessionId, Tipo_Operazione.Logout, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            orm.addLog(l)

            return nDelete, True
        except Exception as ex:
            print(ex.__str__())
        return False

    @staticmethod
    def reg_download(request):
        sessionID = request[4:20]
        md5_file = request[20:52]
        ip = request[52:67]
        port = request[67:72]
        orm = ORM()
        try:
            id_peer = orm.selectPeer(ip, port)
            id_file = orm.selectIDfile(id_peer, md5_file)
            orm.addDownload(sessionID, id_file)
            nDownload = orm.countDownload(md5_file)
            l = Log(sessionID, Tipo_Operazione.DownloadFile, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            orm.addLog(l)
            return nDownload, True   
        except Exception as ex:
            print(ex.__str__())
        return -1, False
