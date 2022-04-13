import unittest
from file import *
from peer import *
from utilities import *

#unit test classe file
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

#unit test classe peer
class TestPeer(unittest.TestCase):
    def test_set_ip(self):
        peer = Peer("192.168.1.1", 80)
        new_ip = "172.16.1.1"
        peer.set_ip(new_ip)
        ip_peer = peer.get_ip()
        self.assertEqual(ip_peer, new_ip, "Should be 172.16.1.1")
    def test_set_port(self):
        peer = Peer("192.168.1.1", 80)
        new_port = 443
        peer.set_port(new_port)
        port_peer = peer.get_port()
        self.assertEqual(port_peer, new_port, "Should be 443")
    def test_get_ip(self):
        peer = Peer("192.168.1.1", 80)
        ip_peer = peer.get_ip()
        self.assertEqual(ip_peer, "192.168.1.1", "Should be 192.168.1.1")
    def test_get_port(self):
        peer = Peer("192.168.1.1", 80)
        port_peer = peer.get_port()
        self.assertEqual(port_peer, 80 , "Should be 80")

#unit test classe utilities
class TestUtilities(unittest.TestCase):
    def test_formatIp(self):
        ip = "192.168.1.1"
        result = Utilities.formatIp(ip)
        self.assertEqual(result, "192.168.001.001", "Should be 192.168.001.001")
    def test_formatPort(self):
        port = 80
        result = Utilities.formatPort(port)
        self.assertEqual(result, "00080", "Should be 00080")

    def test_get_md5(self):
        fileName = "file.py"
        md5_file = "cdbf5597550e706896d49f2e37a4158b"
        result = Utilities.get_md5(fileName)
        self.assertEqual(md5_file, result, "Should be cdbf5597550e706896d49f2e37a4158b")

#da fare test file client alla fine

if __name__ == "__main__":
    unittest.main()
