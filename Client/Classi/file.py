import hashlib

class File:
    
    def __init__(self, fileName, MD5):
        self.fileName = fileName
        self.MD5 = MD5
        self.peers = []

    def check_md5(self, md5):
        result = False
        md5_file = self.MD5
        if(md5 == md5_file):
            result = True
        return result

    def addPeers(self, peers):
        self.peers.append(peers)
