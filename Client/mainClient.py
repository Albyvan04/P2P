from logging import exception
from Classi.client import Client
from Classi.utilities import Utilities
from Classi.file import File
from Classi.peer import Peer
import socket
import sys
import random
import os

#ARGV
#ARGV[0] = null
#ARGV[1] = IP SERVER

# Verifica dei dati immessi

if (len(sys.argv) != 2):
    print("\nI parametri passati non sono corretti.\nFormato nomeFile ipServer.")
    exit(0)

PORTASERVER = 80
CHUNKLEN = 4096
ipServer = sys.argv[1]

#memorizzo i file nella cartella da condividere
files = Utilities.readSharedFiles()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ipServer, PORTASERVER))
except:
    print("Errore di connessione al server")
    exit(0)
else:
    print("Connesso al server")

ipClient = Utilities.formatIp(s.getsockname()[0])
portaClient = Utilities.formatPort(str(random.randint(49152,65535)))

sessionID = Client.login(s, ipClient, portaClient)
print("Il mio SESSION ID: %s" %sessionID)

#genero un secondo processo per gestire il download da altri peer
pid = os.fork()

if(pid != 0):

    Client.showMenu()

    option = int(input())

    while(True):

        if(option == 1):
            files = Utilities.readSharedFiles()
            Client.addFile(s, sessionID, files)

        elif(option == 2):
            Client.removeFile(s, sessionID, files)

        elif(option == 3):
            searchedFiles = Client.searchFile(s, sessionID)
            
        elif(option == 4):
            Client.downloadMenu()

            option = int(input())

            if (option == 1):
                print("\nInserisci un md5:")
                downloadMD5 = input()
                print("\nInserisci nome del file:")
                fileNameDownload = input()
                print("\nInserisci ip peer:")
                ip = input()
                print("\nInserisci porta peer:")
                port = input()
                
                serverDownload = Peer(ip, port)

            elif(option == 2):
                if(len(searchedFiles) != 0):
                    Client.showFilesData(searchedFiles)
                    print("\nScegli una file: ")
                    optionFile = int(input())
                    print("\nScegli una peer: ")
                    optionPeer = int(input())
                    fileNameDownload = searchedFiles[optionFile -1].fileName.replace('|', '')
                    downloadMD5 = searchedFiles[optionFile -1].MD5
                    serverDownload = searchedFiles[optionFile - 1].peers[optionPeer - 1] 
                else:
                    print("\nDevi prima fare una ricerca")
                

            if serverDownload.ip != "":

                socketDownload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socketDownload.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                print(serverDownload.ip, serverDownload.port)

                try:
                    print (Utilities.formatIpDownload("192.168.002.095"))
                    socketDownload.connect((Utilities.formatIpDownload(serverDownload.ip), int(serverDownload.port)))
                except Exception as ex :
                    print("Errore di connessione al servizio di download")
                    print(ex.__str__())
                    exit(0)
                else:
                    print("Connesso al servizio di download")

                request = "RETR" + downloadMD5
                socketDownload.send(request.encode())


                fd = open("receivedFiles/" + fileNameDownload, "wb")

                print("Ricezione di %s" % fileNameDownload)

                response = socketDownload.recv(10)
                chunkNumber = int(response[4 : 10])

                for i in range(chunkNumber):
                    chunckLen = int(socketDownload.recv(5))
                    buf = socketDownload.recv(chunckLen)
                    fd.write(buf)

                fd.close()
                socketDownload.close()

                receivedFileMd5 = Utilities.get_md5("receivedFiles/" + fileNameDownload)


                #controllo ricezione
                if(receivedFileMd5 == downloadMD5):
                    print("File ricevuto correttamente")
                    Client.reg_download(s, sessionID, receivedFileMd5, serverDownload.ip, serverDownload.port)
                else:
                    print("Ricezione file errata")
                    os.remove(fileNameDownload)
            
        elif(option == 5):
            Client.logout(s, sessionID)
            s.close()
            exit()



        Client.showMenu()

        option = int(input())

else:

    socketDownload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketDownload.bind(('', int(portaClient)))
    socketDownload.listen(10)
    print("In ascolto di richieste di download...")

    while True:

        peerSocket, clientAddress = socketDownload.accept()
        print("Richiesta accettata")

        #gestione download concorrente
        pid = os.fork()
        if pid == 0:
        
            request = str(peerSocket.recv(4096).decode())

            if(request[0 : 4] == "RETR"):

                md5 = request[4 : 36]

                for file in files:
                    if(file.MD5 == md5):
                        filename = file.fileName

                fd = open("sharedFiles/" + filename, "rb")

                chunks = b''
                chunkNumber = 0

                while True:

                    buf = fd.read(CHUNKLEN)

                    if len(buf) == 0:
                        print("brekka tutto")
                        break

                    chunks = chunks + str('%05d' % len(buf)).encode() + buf
                    print(str(len(chunks)) + "\n")
                    #print(chunks)
                    
                    chunkNumber += 1
                
                request = ("ARET" + str('%06d' % chunkNumber)).encode() + chunks

                peerSocket.sendall(request)

                fd.close()
            
            print("Connessione chiusa\n")

            peerSocket.close()
            
            print("In ascolto di richieste di download...")

            os._exit(1)
