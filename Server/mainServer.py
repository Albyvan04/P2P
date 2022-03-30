import os
import socket
from Classi.server import Server


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 50000))
s.listen(10)

while True:

    clientSocket, clientAddress = s.accept()
    print("Request accepted")

    pid = os.fork()
    if pid==0:

      request = str(clientSocket.recv(4096).decode())

      if(request[0:4] == "LOGI"):
        Server.login(clientSocket)

      clientSocket.close()
      os._exit(1)
