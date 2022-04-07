#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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
CHUNKLEN = 4096-15
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

            request = "RETR" + "e8cfd85c5430eeef927e33ee4a11562e"
            socketDownload.send(request.encode())

            fd = open("prova.txt", "wb")

            print("Ricezione di %s" % "prova.txt")

            while True:
                response = socketDownload.recv(15 + CHUNKLEN)
                print(len(response))
                buf = response[15 : 15 + int(response[10 : 15].decode())]
                if len(buf) == 0:
                    break
                fd.write(buf)
            fd.close()
            print("sara")
            socketDownload.close()
            
        elif(option == 5):
            Client.logout(s, sessionID)


        Client.showMenu()

        option = int(input())

    s.close()

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
                    if(file.fileMd5 == md5):
                        filename = file.fileName

                fd = open("sharedFiles/" + filename, "rb")

                chunkIndex = 0
                while True:
                    buf = fd.read(CHUNKLEN)
                    request = ("ARET" + str('%06d' % chunkIndex) +  str('%05d' % CHUNKLEN)).encode() + buf
                    print(len(request))
                    peerSocket.send(request, CHUNKLEN + 15)
                    chunkIndex += 1
                    if len(buf) == 0:
                        print("brekka tutto")
                        break

                fd.close()
            
            print("Connessione chiusa\n")

            peerSocket.close()
            
            print("In ascolto di richieste di download...")

            os._exit(1)


