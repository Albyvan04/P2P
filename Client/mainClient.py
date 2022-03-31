from Classi.client import Client
from Classi.utilities import Utilities
import socket
import sys
import random

# Verifica dei dati immessi

if (len(sys.argv) != 2):
    print("\nI parametri passati non sono corretti.\nFormato nomeFile ipServer.")
    exit(0)

PORTASERVER = 50001
ipServer = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ipServer, PORTASERVER))
except:
    print("Errore di connessione al server")
    exit(0)
else:
    print("Connesso al server")

ipClient = Utilities.formatIp(s.getsockname()[0])
portaClient = Utilities.formatPort(str(random.randint(49152,65535)))

sessionID = Client.login(s, ipClient, portaClient)

Client.showMenu()

option = int(input())

while(option!= 5):

    if(option == 1):
        Client.addFile(s, sessionID)

    Client.showMenu()

    option = int(input())

s.close()

