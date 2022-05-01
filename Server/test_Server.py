from datetime import datetime
from Classi.download import Download
from Classi.file import File
from Classi.log import Log
from Classi.orm import ORM, Tipo_Operazione
from Classi.peer import Peer
from Classi.server import Server
from Classi.utilitiesServer import Utilities
import unittest
from ctypes import sizeof
import time

class TestDownload(unittest.TestCase): #FUNZIONA
    def test_get_sessionID(self):
        download = Download("2394be2e1263dcd5b566494fa5d11359", "c26679467622336004c6b6a86a91248c")
        sessionID = download.sessionId
        self.assertEqual(sessionID, "2394be2e1263dcd5b566494fa5d11359", "Should be 2394be2e1263dcd5b566494fa5d11359")
    def test_get_md5file(self):
        download = Download("2394be2e1263dcd5b566494fa5d11359", "c26679467622336004c6b6a86a91248c")
        md5 = download.md5file
        self.assertEqual(md5, "c26679467622336004c6b6a86a91248c", "Should be c26679467622336004c6b6a86a91248c")

class TestFile(unittest.TestCase): #FUNZIONA
    def test_get_md5(self):
        file = File("mainServer.py", "0ffd3669ab8f43d37f5d64e292666431")
        result = file.get_md5()
        self.assertEqual("0ffd3669ab8f43d37f5d64e292666431", result, "Should be 0ffd3669ab8f43d37f5d64e292666431")

    def test_check_md5(self):
        file = File("mainServer.py", "0ffd3669ab8f43d37f5d64e292666431")
        md5 = file.get_md5()
        result = file.check_md5(md5)
        self.assertEqual(result, True, "Should be True")

class TestLog(unittest.TestCase):
    def test_log(self):
        sessionID = "a"
        tipo_operazione = "login"
        data = time.strftime("%d%m%Y")
        ora = time.strftime("%H:%M:%S")
        log = Log(sessionID, tipo_operazione, data, ora)
        self.assertEqual(log.sessionID, sessionID, "Should be a")
        self.assertEqual(log.tipo_operazione, tipo_operazione, "Should be login")

class TestServer(unittest.TestCase):
    def test_login(self):
       request = "LOGI192.168.000.00100080"
       result, bol = Server.login(request)
       peer = result
       self.assertEqual(bol, True, "Should be True")
       ip = peer.ip
       port = peer.port
       self.assertEqual(ip, "192.168.000.001", "Should be 192.168.000.001")
       self.assertEqual(port, "00080", "Should be 00080")

    def test_addFile(self):
        request = "ADDF5bbffd9a2eb953f8a29725db56e7fbe736169fa563ca8506b7f4e642fd2e000063777b455f0e9447288a1c0d505f9d8d8c7cf4f817eedc98f2642474bf0996e421e07ba775431e4664eff62956023cae8fd3819e5dcd3cf7d808963f83b74f0d4922a224b95c96d29b1eeddfd5c055e9827cd7ecd1e05dc514f651f6b078d390f4dd05fa25d81383455d338c2b1d292247e68025"
        nCopia, bol = Server.addFile(request)
        self.assertEqual(nCopia, 0, "Should be 0")
        self.assertEqual(bol, True, "Should be True")

    def test_logout(self):
        request = "LOGO00d740310ffa0758804a365822765076"
        result = Server.logout(request)
        self.assertEqual(result, True, "Should be True")

    def test_regDownload(self):
        request = "RREG00d740310ffa0758804a36582276507661799a05862487433fbe1643f774c87a78cdaeb5c669df7e4640bbeb5f8c90d627067c598655eebd62b8151b5a54637b81d25d22"
        i, bol = Server.reg_download(request)
        self.assertEqual(i, -1 , "Should be -1")
        self.assertEqual(bol, False, "Should be False")


if __name__ == "__main__":
    unittest.main()
