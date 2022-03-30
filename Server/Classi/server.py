import socket
from utilities import Utilities

class Server:

    @staticmethod
    def login(socket):
        sessionId = Utilities.generateSessionID()
        socket.send(bytes(("ALGI" + sessionId).encode()))