import os
import socket
from Classi.server import Server
from Classi.utilitiesServer import Utilities


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 50001))
s.listen(10)

while True:

    clientSocket, clientAddress = s.accept()
    print("Richiesta accettata")

    pid = os.fork()
    if pid==0:

      continueCicle = True

      while(continueCicle):

        request = str(clientSocket.recv(4096).decode())

        #print(len(request.encode()))

        if(request[0:4] == "LOGI"):
          Server.login(clientSocket)
          print("Login")
        elif(request[0:4] == "ADDF"):
          Server.addFile(clientSocket)
          print("AddFile")
        elif(request[0:4] == "DELF"):
          Server.removeFile(clientSocket)
        elif(request[0:4] == "FIND"):
          Server.searchFile(clientSocket)
        elif(request[0:4] == "RETR"):
          Server.download(clientSocket)
        elif(request[0:4] == "LOGO"):
          Server.logout(clientSocket)
          continueCicle = False


      print("Connessione chiusa\n")
      clientSocket.close()
      os._exit(1)
