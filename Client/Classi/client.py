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
        response = socket.recv(4096).decode()
        return response[4 : 20] if response[0: 4] == "ALGI" else exit("Server login failed")

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
    def searchFile(socket, sessionId):
        return ""

    @staticmethod
    def download(socket, sessionId):
        #effettuare una ricerca e far selezionare il peer da cui fare download
        #segnalazione al server dell'operazione
        return Peer("25.72.89.220", 53000)


    @staticmethod
    def logout(socket, sessionId):
        request = "LOGO" + sessionId
        socket.send(request.encode())
        response = socket.recv(4096).decode()
        print("Logout effettuato") if response[0: 4] == "ALGO" else exit("Server logout failed")


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