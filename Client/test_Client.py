import unittest
from Classi.client import *
from Classi.file import *
from Classi.peer import *
from Classi.utilities import *
import socket

class TestClient(unittest.TestCase):
    def test_login(self): #DA RIVEDERE
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipClient = Utilities.formatIp("192.168.0.1")
        portClient = Utilities.formatPort(80)
        result = Client.login(s, ipClient, portClient)
        self.assertEqual(result, "", "Should be ")
