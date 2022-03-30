import hashlib

class File:
    def __init__(self, fileName, filePath):
        self.fileName = fileName
        self.filePath = filePath

    def get_md5 (self):
        file = open(self.fileName, 'rb')
        dati = file.read()
        md5 = ''
        md5 = hashlib.md5(dati).hexdigest()
        return md5

    def check_md5(self, md5):
        result = False
        md5_file = self.get_md5()
        if(md5 == md5_file):
            result = True
        return result
