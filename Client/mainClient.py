from ctypes import sizeof
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
CHUNKLEN = 2048
ipServer = sys.argv[1]

#memorizzo i file nella cartella da condividere
files = []
filesName = os.listdir("sharedFiles")
for fileName in filesName:
    fileMd5 = Utilities.get_md5(fileName)
    print(fileMd5)
    files.append(File(fileName, fileMd5))       

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ipServer, PORTASERVER))
except:
    print("Errore di connessione al server")
    exit(0)
else:
    print("Connesso al server")

ipClient = Utilities.formatIp(s.getsockname()[0])
#portaClient = Utilities.formatPort(str(random.randint(49152,65535)))
portaClient = "53000"

sessionID = Client.login(s, ipClient, portaClient)

#genero un secondo processo per gestire il download da altri peer
pid = os.fork()

if(pid != 0):

    Client.showMenu()

    option = int(input())

    while(option!= 5):

        if(option == 1):
            Client.addFile(s, sessionID, files)
        elif(option == 2):
            Client.removeFile(s, sessionID)
        elif(option == 3):
            Client.searchFile(s, sessionID)
        elif(option == 4):
            serverDownload = Client.download(s, sessionID)

            socketDownload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(serverDownload.get_ip(), serverDownload.get_port())

            try:
                socketDownload.connect((serverDownload.get_ip(), serverDownload.get_port()))
            except:
                print("Errore di connessione al servizio di download")
                exit(0)
            else:
                print("Connesso al servizio di download")

            request = "RETR" + "05d8e48a27ac2a98cf2c74e391689552"
            socketDownload.send(request.encode())

            fd = os.open("prova.deb", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o777)

            print("Ricezione di %s" % "prova.txt")

            while True:
                response = socketDownload.recv(CHUNKLEN + 15)
                print(response)
                buf = response[15 : 15 + CHUNKLEN]
                if not buf:
                    break
                os.write(fd, buf)
            socketDownload.close()
            
        elif(option == 5):
            Client.logout(s, sessionID)


        Client.showMenu()

        option = int(input())

    s.close()

else:

    socketDownload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketDownload.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                    if(file.fileMd5 == md5):
                        filename = file.fileName

                fd = os.open("sharedFiles/" + filename, os.O_RDONLY)

                chunkIndex = 0
                while True:
                    buf = os.read(fd, CHUNKLEN).decode()
                    if not buf:
                        break
                    request = "ARET" + str('%06d' % chunkIndex) +  str('%05d' % CHUNKLEN) + buf
                    print(request)
                    print(request.encode())
                    peerSocket.send(request.encode(), CHUNKLEN + 15)
                    chunkIndex += 1

                os.close(fd)
            
            print("Connessione chiusa\n")
            peerSocket.close()
            os._exit(1)
