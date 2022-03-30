import os
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 50000))
s.listen(10)

while True:
    conn, addr = s.accept()
    print("connesso")
    pid = os.fork()
    if pid==0:
      conn.close()
      os._exit(1)
