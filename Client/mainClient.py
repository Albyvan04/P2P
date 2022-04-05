from Classi.client import Client
from Classi.utilities import Utilities
from Classi.file import File
import socket
import sys
import random
import os

# Verifica dei dati immessi

if (len(sys.argv) != 2):
    print("\nI parametri passati non sono corretti.\nFormato nomeFile ipServer.")
    exit(0)

PORTASERVER = 50001
ipServer = sys.argv[1]

#memorizzo i file nella cartella da condividere
files = []
filesName = os.listdir("sharedFiles")
for fileName in filesName:
    fileMd5 = Utilities.get_md5(fileName)
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
portaClient = Utilities.formatPort(str(random.randint(49152,65535)))

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
            Client.download(s, sessionID)
        elif(option == 5):
            Client.logout(s, sessionID)


        Client.showMenu()

        option = int(input())

    s.close()

else:

    socketDownload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketDownload.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketDownload.bind(('', portaClient))
    socketDownload.listen(10)
    print("In ascolto di richieste di download...")

    while True:

        peerSocket, clientAddress = socketDownload.accept()
        print("Richiesta accettata")

        #gestione download concorrente
        pid = os.fork()
        if pid == 0:
            

            # fd = os.open(filename, os.O_RDONLY)

            while True:
                buf = os.read(fd, 4096)
                if not buf:
                    break
                peerSocket.send(buf)

            os.close(fd)
            s.close()

            
        print("Connessione chiusa\n")
        peerSocket.close()
        os._exit(1)



