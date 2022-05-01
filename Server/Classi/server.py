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
            if (orm.selectIDfile(session_id, md5_file) != None):
                orm.deleteFile(session_id, md5_file)

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

            #elimino il file
            bol = orm.deleteFile(sessionId, md5_file)
            nCopie = orm.selectCopyFile(md5_file)
            if(bol == True):
                l = Log(sessionId, Tipo_Operazione.DeleteFile, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
                orm.addLog(l)
                return nCopie, True

            return nCopie, False

        except Exception as ex:
            print(ex.__str__())
        
        return -1, False

    
    @staticmethod
    def searchFile(request):
        sessionId = request[4:20]
        ricercato = request[20:40].replace(' ', '')
        #print(ricercato)

        orm = ORM()

        try:
            filesTmp, bol = orm.selectfile(ricercato)

            if(bol == False):
                return "AFIN000"

            files = []
            index = 0

            for file in filesTmp:

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

                index += 1

            else:

                request = "AFIN" + '%03d' % len(files)

                for file in files:

                    # print("ID = %s\t\t", row[0])
                    # print("Filename = %s\t\t", row[3])
                    # print("MD5 = %s\t\t", row[1])
                    # print("SessionId = %s\t\t", row[2])
                    # print("Copia = %s\t\t", row[4])

                    request += file.MD5 + file.fileName + '%03d' % len(file.peers)

                    for peer in file.peers:
                        request += peer.ip + str(peer.port)
                
                return request

        except Exception as ex:
            print(ex.__str__())


    @staticmethod
    def logout(request):
        sessionId = request[4:20]
        orm = ORM()

        try:
            #conto il numero di file associati a quel peer per restituirlo in risposta
            nFile = orm.countFile(sessionId)
            print("Numero file condivisi: %d"%nFile)
            #elimino i file di quel peer
            orm.deleteAllFile(sessionId)
            if nFile <= 0:
                print("Il peer non ha condiviso nessun file")
            else:
                print("Sono stati rimossi %d file" %nFile)
            #print("Numero file eliminati: %d" %nDelete)
            
            #creo il log
            l = Log(sessionId, Tipo_Operazione.Logout, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            orm.addLog(l)

            #elimino il peer dalla lista
            orm.deletePeer(sessionId)
            return nFile, True
        except Exception as ex:
            print(ex.__str__())
        return -1, False

    @staticmethod
    def reg_download(request):
        sessionID = request[4:20]
        md5_file = request[20:52]
        ip = request[52:67]
        port = request[67:72]
        orm = ORM()
        try:
            peer = orm.selectPPeer(ip, port)
            id_file = orm.selectIDfile(peer.session_id, md5_file)
            orm.addDownload(sessionID, id_file)
            nDownload = orm.countDownload(md5_file)
            l = Log(sessionID, Tipo_Operazione.DownloadFile, time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            orm.addLog(l)
            return nDownload, True   
        except Exception as ex:
            print("serv", ex.__str__())
        return -1, False


