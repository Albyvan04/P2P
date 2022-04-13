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
        socket.send(request.encode())
        #response = socket.recv(4096).decode()
        #return response[4 : 20] if response[0: 4] == "ALGI" else exit("Server login failed")
        return ''

    @staticmethod
    def addFile(socket, sessionID, files):
        files = []
        for file in files:
            request = "ADDF" + sessionID + file.fileMd5 + Utilities.formatString(file.fileName, 100)
            socket.send(request.encode())
            response = socket.recv(4096).decode()
            print("File aggiunto") if response[0: 4] == "AADD" else exit("Server add file failed")


    @staticmethod
    def removeFile(socket, sessionId):
        return ""
    
    @staticmethod
    def searchFile(socket, sessionID):
        print("Inserire il nome del file da cercare: ")

        searchString = Utilities.formatString(input()[0 : 20],20)

        request = "FIND" + sessionID + searchString

        socket.send(request.encode())

        searchedFiles = []

        if socket.recv(4).decode() == "AFIN":
            md5Number = socket.recv(3)
            for i in range(md5Number):
                searchedFiles.append(File(socket.recv(100).decode() , socket.recv(32).decode()))
                peersNumber = socket.recv(3)
                peers = []
                for j in range(peersNumber):
                    peers.append(Peer(socket.recv(15).decode(), socket.recv(5).decode()))
                searchedFiles[i].addPeers(peers)
                
        else:
            exit("Server search file failed")


        Client.showFilesData(searchedFiles)

        return searchedFiles

    @staticmethod
    def showFilesData(files):
        index = 0
        for file in files:
            print("\n=== " + file.fileName + " " + file.MD5)
            for peer in file.peers:
                print("\n     ===" + index + ")" + peer.ip + " " + peer.port)
                index = index + 1

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
        socket.send(request.encode())
        response = socket.recv(4096).decode()
        print("Logout effettuato") if response[0: 4] == "ALGO" else exit("Server logout failed")


    @staticmethod
    def reg_download(socket, sessionId, md5_file, ip, port):
        request = "RREG" + sessionId + md5_file + ip + str(port)
        socket.send(request.encode())
        response = socket.recv(4096).decode()
        print("Download registrato sul server") if response[0: 4] == "ARRE" else exit("Download non registrato")



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
