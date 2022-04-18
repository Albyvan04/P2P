from ctypes import sizeof
import hashlib
from http import server
import unittest
from download import *
from file import *
from log import *
from orm import *
from peer import *
from script import *
from server import *
from utilitiesServer import *

#test classe download funziona
class TestDownload(unittest.TestCase):  
    def test_get_sessionID(self):
        download = Download("2394be2e1263dcd5b566494fa5d11359", "c26679467622336004c6b6a86a91248c")
        sessionID = download.sessionId
        self.assertEqual(sessionID, "2394be2e1263dcd5b566494fa5d11359", "Should be 2394be2e1263dcd5b566494fa5d11359")
    def test_get_md5file(self):
        download = Download("2394be2e1263dcd5b566494fa5d11359", "c26679467622336004c6b6a86a91248c")
        md5 = download.md5file
        self.assertEqual(md5, "c26679467622336004c6b6a86a91248c", "Should be c26679467622336004c6b6a86a91248c")


#test classe File funziona
class TestFile(unittest.TestCase):
    def test_check_md5(self):
        file = File("file.py", "path")
        md5 = file.get_md5()
        result = file.check_md5(md5)
        self.assertEqual(result, True, "Should be True")

    def test_get_md5(self):
        file = File("file.py", "path")
        md5 = "cdbf5597550e706896d49f2e37a4158b"
        md5_ritornato = file.get_md5()
        self.assertEqual(md5_ritornato, md5, "Should be cdbf5597550e706896d49f2e37a4158b")        
        
#forse dopo serve test per classe log

#test classe Peer
class TestPeer(unittest.TestCase):
    def test_set_session_id(self):
        peer = Peer("dba6bca8f6b6bb3365fb2bfe4d440006", "192.168.1.1", 80)
        sessionID = "61b1eb268b8b8c0b51565dc3e63788d5"
        peer.set_session_id(sessionID)
        check_peer_sessionID = peer.get_session_id()
        self.assertEqual(check_peer_sessionID, "61b1eb268b8b8c0b51565dc3e63788d5", "Should be 61b1eb268b8b8c0b51565dc3e63788d5")
       
    def test_set_ip(self):
        peer = Peer("dba6bca8f6b6bb3365fb2bfe4d440006", "192.168.1.1", 80)
        ip = "192.168.1.1"
        peer.set_ip(ip)
        check_ip_peer = peer.get_ip()
        self.assertEqual(check_ip_peer, "192.168.1.1", "Should be 192.168.1.1")
       
    def test_set_port(self):
        peer = Peer("dba6bca8f6b6bb3365fb2bfe4d440006", "192.168.1.1", 80)
        port = 80
        peer.set_port(port)
        check_port_peer = peer.get_port()
        self.assertEqual(check_port_peer, 80, "Should be 80")
        
    def test_get_session_id(self):
        peer = Peer("b5fb4e26e0728593f1e4b8722e141643", "192.168.1.1", 80)
        sessionID = peer.get_session_id()
        self.assertEqual(sessionID, "b5fb4e26e0728593f1e4b8722e141643", "Should be b5fb4e26e0728593f1e4b8722e141643")
        
    def test_get_ip(self):
        peer = Peer("b5fb4e26e0728593f1e4b8722e141643", "192.168.1.1", 80)
        ip = peer.get_ip()
        self.assertEqual(ip, "192.168.1.1", "Should be 192.168.1.1")
       
    def test_get_port(self):
        peer = Peer("b5fb4e26e0728593f1e4b8722e141643", "192.168.1.1", 80)
        port = peer.get_port()
        self.assertEqual(port, 80, "Should be 80")

#test classe utilities server
class TestUtilities(unittest.TestCase):
    def test_generateSessionID(self):
        sessionID = Utilities.generateSessionID()
        lenght = sizeof(sessionID)
        self.assertEqual(sessionID, lenght, "Should be 16")

#test del server
class TestServer(unittest.TestCase):
    def test_login(self, request):
        request = "LOGI000.000.000.00000000"
        bool = Server.login(request)
        sessionID = Utilities.generateSessionID()
        peer = Peer(sessionID, "000.000.000.000", 00000)
        self.assertEqual(bool, (), "Should be True")
        
    def test_logout(self, request):
        request = "LOGI000.000.000.00000000"
        bool = Server.logout(request)
        sessionID = Utilities.generateSessionID()
        peer = Peer(sessionID, "000.000.000.000", 00000)
        self.assertEqual(bool, (peer, True), "Should be True")
        
#    def test_addFile(self, socket): #da sistemare
#        #socket = .....
#        #.....
#        bool = True
#        #self.assertEqual(bool, *....*, "Should be True")
#
#    def test_removeFile(self, socket, sessionID): #da sistemare
#        #socket = .....
#        sessionID = Utilities.generateSessionID()
#        #.....
#        bool = True
#        #self.assertEqual(bool, *....*, "Should be True")
#        
#    def test_searchFile(self, socket, sessionID): #da sistemare
#        #socket = .....
#        sessionID = Utilities.generateSessionID()
#        #.....
#        bool = True
#        #self.assertEqual(bool, *....*, "Should be True")
#        
#    def test_download(self, socket, sessionID): #da sistemare
#        #socket = .....
#        sessionID = Utilities.generateSessionID()
#        #.....
#        bool = True
#        #self.assertEqual(bool, *....*, "Should be True")        

        
             
if __name__ == "__main__":
    unittest.main()
