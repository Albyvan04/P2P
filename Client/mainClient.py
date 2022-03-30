import socket
import sys
import random

#def login(portaClient, ipClent):
    
# Verifica dei dati immessi
print(len(sys.argv))

if (len(sys.argv) != 2):
    print("\nI parametri passati non sono corretti.\nFormato nomeFile ipServer.")
    exit(0)

portaServer = 50000
ipServer = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ipServer, portaServer))
except:
    print("Errore di connessione al server")
    exit(0)
finally:
    print("Connesso al server")

hostname = s.gethostname()
ipClient = s.gethostbyname(hostname)
portaClient = random.randint(50000,52000)

print(ipClient, portaClient)


s.close()

