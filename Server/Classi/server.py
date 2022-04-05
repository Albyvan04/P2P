import socket
from .utilitiesServer import Utilities

class Server:

    @staticmethod
    def login(socket):
        #aggiungere in database
        socket.send(("ALGI" + Utilities.generateSessionID()).encode())

    @staticmethod
    def addFile(socket):
        #aggiungere in database
        socket.send(("AADD").encode()) #manca attributo

    @staticmethod
    def removeFile(socket, sessionId):
        return ""
    
    @staticmethod
    def searchFile(socket, sessionId):
        return ""

    @staticmethod
    def download(socket, sessionId):
        return ""

    @staticmethod
    def logout(socket, sessionId):
        #rimuovo da database
        socket.send(("ALGO").encode()) #manca attributo


    