import socket
import os
from urllib import request
from .file import File
from .utilities import Utilities
from .peer import Peer

class Client:

    @staticmethod
    def login(socket, ipClient, portaClient):
        request = "LOGI" + ipClient + portaClient
        print(">%s" %request)
        socket.send(request.encode())
        response = socket.recv(4096).decode()
        print("<%s" %response)
        return response[4 : 20] if response[0: 4] == "ALGI" else exit("Server login failed")

    @staticmethod
    def addFile(socket, sessionID, files):
        #files = []
        for file in files:
            request = "ADDF" + sessionID + file.MD5 + Utilities.formatString(file.fileName, 100)
            print(">%s" %request)
            socket.send(request.encode())
            response = socket.recv(4096).decode()
            print("<%s" %response)
            print("File aggiunto") if response[0: 4] == "AADD" else print("Server add file failed")


    @staticmethod
    def removeFile(socket, sessionId, files):
        print("Inserire md5 del file da rimuovere: ")
        removeMd5 = input()[0:32]
        request = "DELF" + sessionId + removeMd5
        socket.send(request.encode())
        response = socket.recv(4096).decode()
        updateFiles = []
        for file in files:
            fileMd5 = Utilities.get_md5("sharedFiles/" + file.fileName)
            if fileMd5 != removeMd5:
                file = File(file.fileName, fileMd5)
                updateFiles.append(file)
        files = updateFiles
        print("File rimosso") if response[0:4] == "ADEL" else print("Server remove file failed")
    
    @staticmethod
    def searchFile(socket, sessionID):
        print("Inserire il nome del file da cercare: ")

        searchString = Utilities.formatString((input()[0 : 20]).strip(),20)

        request = "FIND" + sessionID + searchString

        socket.send(request.encode())

        searchedFiles = []

        if socket.recv(4).decode() == "AFIN":
            md5Number = socket.recv(3)
            for i in range(md5Number):
                md5 = socket.recv(32).decode()
                filename = socket.recv(100).decode()
                searchedFiles.append(File(filename, md5))
                peersNumber = socket.recv(3)
                peers = []
                for j in range(peersNumber):
                    peers.append(Peer(socket.recv(15).decode(), socket.recv(5).decode()))
                searchedFiles[i].addPeers(peers)
                
        else:
            print("Server search file failed")


        Client.showFilesData(searchedFiles)

        return searchedFiles

    @staticmethod
    def showFilesData(files):
        indexFile = 1
        indexPeer = 1
        for file in files:
            print("\n===" + indexFile + ")" + file.fileName + " " + file.MD5)
            indexFile += 1
            for peer in file.peers:
                print("\n     ===" + indexPeer + ")" + peer.ip + " " + peer.port)
                indexPeer += 1

    @staticmethod
    def downloadMenu():
        print("\n= = = = = = = = =")
        print("\n D O W N L O A D")
        print("\n= = = = = = = = =")
        print("\n1) Inserisci md5 e credenziali peer manualmente")
        print("\n2) Usa i dati della precendente ricerca")
        print("\nScegli una opzione: ")


    @staticmethod
    def logout(socket, sessionId):
        request = "LOGO" + sessionId
        print(">%s" %request)
        socket.send(request.encode())
        response = socket.recv(4096).decode()
        print("<%s" %response)
        print("Logout effettuato") if response[0: 4] == "ALGO" else print("Server logout failed")


    @staticmethod
    def reg_download(socket, sessionId, md5_file, ip, port):
        request = "RREG" + sessionId + md5_file + ip + str(port)
        socket.send(request.encode())
        response = socket.recv(4096).decode()
        print("Download registrato sul server") if response[0: 4] == "ARRE" else print("Download non registrato")



    @staticmethod
    def showMenu():
        print("\n= = = = = = = = =")
        print("\n     M E N Ù     ")
        print("\n= = = = = = = = =")
        print("\n1) Aggiungi file")
        print("\n2) Rimuovi file")
        print("\n3) Cerca file")
        print("\n4) Download")
        print("\n5) Logout")
        print("\nScegli una opzione: ")
