import hashlib

class File:
    
    def __init__(self, fileName, MD5):
        self.fileName = fileName
        self.MD5 = MD5

    def check_md5(self, md5):
        result = False
        md5_file = self.get_md5()
        if(md5 == md5_file):
            result = True
        return result

    def addPeers(self, peers):
        self.peers = peers
