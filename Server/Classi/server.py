import socket
from .utilitiesServer import Utilities

class Server:

    @staticmethod
    def login(socket):
        #aggiungere in database
        socket.send(("ALGI" + Utilities.generateSessionID()).encode())

    @staticmethod
    def addFile(socket, request):
        #aggiungere in database
        socket.send(("AADD").encode()) #manca attributo

    @staticmethod
    def removeFile(socket, request):
        return ""
    
    @staticmethod
    def searchFile(socket,  request):
        return ""

    @staticmethod
    def download(socket, request):
        return ""

    @staticmethod
    def logout(socket, request):
        #rimuovo da database
        socket.send(("ALGO").encode()) #manca attributo


    