import socket
import sys
import random

def formatIp(IP):
    ipSplitted = IP.split('.')
    i= 0
    while(i < len(ipSplitted)):
        ipSplitted[i] = '%03d' % int(ipSplitted[i])
        i += 1
    return '.'.join(ipSplitted)



def login(socket, portaClient, ipClient):
    request = "LOGI" + ipClient + portaClient
    print(bytes(request))
    #s.send(bytes(request))


    
# Verifica dei dati immessi
print(len(sys.argv))

if (len(sys.argv) != 2):
    print("\nI parametri passati non sono corretti.\nFormato nomeFile ipServer.")
    exit(0)

PORTASERVER = 50000
ipServer = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ipServer, PORTASERVER))
except:
    print("Errore di connessione al server")
    exit(0)
finally:
    print("Connesso al server")

ipClient = s.getsockname()[0]
portaClient = random.randint(50000,52000)

login(s, formatIp(ipClient), portaClient)

s.close()

