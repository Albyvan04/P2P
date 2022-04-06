import os
import socket
from Classi.server import Server
from Classi.utilitiesServer import Utilities

try:
    exec(open(os.path.dirname(__file__) + "/Classi/script.py").read())
except Exception as ex:
    print("%s" %ex)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(10)
print("In ascolto...")

while True:

    clientSocket, clientAddress = s.accept()
    print("Richiesta accettata")

    pid = os.fork()
    if(pid == 0):

      continueCicle = True

      while(continueCicle):

        request = str(clientSocket.recv(4096).decode())

        #print(len(request.encode()))        

        #region LOGIN
        if(request[0:4] == "LOGI"): #login

          #elaborazione della richiesta
          peer, bol = Server.login(request)

          if (bol == True):
            print("Login effettuato")

            #risposta del server
            clientSocket.send(("ALGI" + peer.get_session_id()).encode())

          else:
            print("Login fallito")
        #endregion

        #region ADD FILE
        elif(request[0:4] == "ADDF"):
          Server.addFile(clientSocket, request)
          print("AddFile")
        #endregion

        #region REMOVE FILE
        elif(request[0:4] == "DELF"):
          Server.removeFile(clientSocket, request)
        #endregion

        #region FIND FILE
        elif(request[0:4] == "FIND"):
          Server.searchFile(clientSocket, request)
        #endregion

        #region DOWNLOAD FILE
        elif(request[0:4] == "RETR"):
          Server.download(clientSocket, request)
        #endregion

        #region LOGOUT
        elif(request[0:4] == "LOGO"): #logout

          #elaborazione della richiesta
          if(Server.logout(request) == True):
            print("Logout effettuato")

            #risposta al client
            clientSocket.send(("ALGO").encode()) #manca attributo
            continueCicle = False

          else:
            print("Logout fallito")
        #endregion

      print("Connessione chiusa\n")
      clientSocket.close()
      os._exit(1)
