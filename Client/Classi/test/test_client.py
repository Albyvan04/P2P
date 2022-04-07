import unittest
from file import *
from peer import *
from utilities import *

#unit test classe file
class TestFile(unittest.TestCase):
    def test_check_md5(self, file, md5):
        file = File("file.py", "4c58febf1ac7d8fd831b7494655734df")
        result = file.check_md5("4c58febf1ac7d8fd831b7494655734df")
        self.assertEqual(result, True, "Should be True")

#unit test classe peer
class TestPeer(unittest.TestCase):
    def test_set_ip(self, peer):
        peer = Peer("192.168.1.1", 80)
        new_ip = "172.16.1.1"
        peer.set_ip(new_ip)
        ip_peer = peer.get_ip()
        self.assertEqual(ip_peer, new_ip, "Should be 172.16.1.1")

    def test_set_port(self, peer):
        peer = Peer("192.168.1.1", 80)
        new_port = 443
        peer.set_port(new_port)
        port_peer = peer.get_port()
        self.assertEqual(port_peer, new_port, "Should be 443")

    def test_get_ip(self, peer):
        peer = Peer("192.168.1.1", 80)
        ip_peer = peer.get_ip()
        self.assertEqual(ip_peer, "192.168.1.1", "Should be 192.168.1.1")

    def test_get_port(self, peer):
        peer = Peer("192.168.1.1", 80)
        port_peer = peer.get_port()
        self.assertEqual(port_peer, 80 , "Should be 80")

#unit test classe utilities
class TestUtilities(unittest.TestCase):
    def test_formatIp(self, ip):
        ip = "192.168.1.1"
        ipSplitted = ip.split('.')
        result = Utilities.formatIp(ip)
        self.assertEqual('.'.join(ipSplitted), result, "Should be %s" %('.'.join(ipSplitted)))

    def test_get_md5(self, fileName):
        fileName = "file.py"
        md5_file = "4c58febf1ac7d8fd831b7494655734df"
        result = Utilities.get_md5(fileName)
        self.assertEqual(md5_file, result, "Should be 4c58febf1ac7d8fd831b7494655734df")

#da fare test file client alla fine

if __name__ == "__main__":
    unittest.main()
