import socket

class Client:

    @staticmethod
    def login(socket, ipClient, portaClient):
        request = "LOGI" + ipClient + portaClient
        socket.send(bytes(request.encode()))
        response = socket.recv(4096).decode()
        return response[5 : 21] if response[0: 4] == "ALGI" else exit("Server login response failed")