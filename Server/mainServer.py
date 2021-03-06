import os
from pydoc import cli
import socket
from Classi.server import Server
from Classi.utilitiesServer import Utilities

try:
    exec(open("Classi/script.py").read())
except Exception as ex:
    print("%s" %ex)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(10)
print("In ascolto...")

while True:

    clientSocket, clientAddress = s.accept()
    print("Richiesta accettata")
    print(clientAddress)

    pid = os.fork()
    if(pid == 0):

      continueCicle = True

      while(continueCicle):

        request = str(clientSocket.recv(4096).decode())

        #region LOGIN
        if(request[0:4] == "LOGI"): #login

          #elaborazione della richiesta
          peer, bol = Server.login(request)

          if (bol == True):
            print("Login effettuato")

            #risposta del server
            clientSocket.send(("ALGI" + peer.session_id).encode())

          else:
            clientSocket.send(("ALGI" + "0000000000000000").encode())
            print("Login non riuscito")
        #endregion

        #region ADD FILE
        elif(request[0:4] == "ADDF"):

          #elaborazione richiesta
          nCopia, bol = Server.addFile(request)

          if (bol == True):
            print("File aggiunto correttamente")

            #risposta del server
            clientSocket.send(("AADD").encode() + ('%03d' % nCopia).encode())

          else:
            print("Problema nell'aggiunta del file")

        #endregion

        #region REMOVE FILE
        elif(request[0:4] == "DELF"):

          nCopie, bol = Server.removeFile(request)

          if (bol == True):
            print("File rimosso correttamente")

            #risposta del server
          else:
            print("Problema con la rimozione del file")

          clientSocket.send(("ADEL").encode() + ('%03d' % nCopie).encode())

        #endregion

        #region FIND FILE
        elif(request[0:4] == "FIND"):

          request = Server.searchFile(request)

          clientSocket.send(request.encode())
        #endregion

        #region LOGOUT
        elif(request[0:4] == "LOGO"): #logout
          #elaborazione della richiesta
          nDelete, bol = Server.logout(request)

          if(bol == True):
            print("Logout effettuato")

            #risposta al client
            clientSocket.send(("ALGO").encode() + ('%03d' % nDelete).encode())
            continueCicle = False

            clientSocket.close()
          else:
            print("Logout fallito")
        #endregion

        #region DOWNLOAD_REGISTRATION

        elif(request[0:4] == "RREG"):
          result, bol = Server.reg_download(request)
          if(bol == True):
            print("Download registrato")
            clientSocket.send(("ARRE").encode() + ('%05d' % int(result)).encode())
          else:
            print("Download non registrato")
           
        #endregion

      print("Connessione chiusa\n")
      clientSocket.close()
      os._exit(1)

