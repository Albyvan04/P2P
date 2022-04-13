from http import server
import unittest
from Classi.server import *
from Classi.peer import *
from Classi.download import *
from Classi.file import *
from Classi.log import *
from Classi.orm import *
from Classi.script import *

class TestServer(unittest.TestCase):
    def test_login(self):
       request = "LOGI192.168.000.00100080"
       result, bol = Server.login(request)
       peer = result
       self.assertEqual(bol, False, "Should be False")
       ip = peer.get_ip()
       port = peer.get_port()
       self.assertEqual(ip, "192.168.000.001", "Should be 192.168.000.001")
       self.assertEqual(port, "00080", "Should be 00080")

    def test_addFile(self):
        request = "ADDF5bbffd9a2eb953f8a29725db56e7fbe736169fa563ca8506b7f4e642fd2e000063777b455f0e9447288a1c0d505f9d8d8c7cf4f817eedc98f2642474bf0996e421e07ba775431e4664eff62956023cae8fd3819e5dcd3cf7d808963f83b74f0d4922a224b95c96d29b1eeddfd5c055e9827cd7ecd1e05dc514f651f6b078d390f4dd05fa25d81383455d338c2b1d292247e68025"
        nCopia, bol = Server.addFile(request)
        self.assertEqual(nCopia, -1, "Should be -1")
        self.assertEqual(bol, False, "Should be False") 

    #def test_removeFile(self): DA RIVEDERE
    #    request = "DELF91e563b059504597a7105cb3b5ca3e831ee392edaa56916b064a8ba6b070eeebdba69d5b0e1e090d1e398336d022175a"
    #    nCopie, bol = Server.removeFile(request)
    #    self.assertEqual(bol, False, "Should be False")


if __name__ == "__main__":
    unittest.main()