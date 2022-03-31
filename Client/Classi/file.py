
class File:
    def __init__(self, fileName, fileMd5):
        self.fileName = fileName
        self.fileMd5 = fileMd5


    def check_md5(self, md5):
        result = False
        md5_file = self.get_md5()
        if(md5 == md5_file):
            result = True
        return result
