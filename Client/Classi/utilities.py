import hashlib
import re
import os
from .file import File

class Utilities:

    @staticmethod
    def formatIp(ip):
        ipSplitted = ip.split('.')
        i= 0
        while(i < len(ipSplitted)):
            ipSplitted[i] = '%03d' % int(ipSplitted[i])
            i += 1
        return '.'.join(ipSplitted)

    @staticmethod
    def formatIpDownload(ip):
        ipSplitted = ip.split('.')
        i= 0
        while(i < len(ipSplitted)):
            ipSplitted[i] = '%01d' % int(ipSplitted[i])
            i += 1
        return '.'.join(ipSplitted)

    @staticmethod
    def readSharedFiles():
        files = []
        filesName = os.listdir("sharedFiles")
        for fileName in filesName:
            fileMd5 = Utilities.get_md5("sharedFiles/" + fileName)
            file = File(fileName, fileMd5)
            print("%s %s" %(file.fileName, file.MD5))
            files.append(File(fileName, fileMd5))
        return files



    @staticmethod
    def formatPort(port):
        return '%05d' % int(port)


    @staticmethod
    def get_md5 (fileName):
        file = open(fileName, 'rb')
        dati = file.read()
        md5 = ''
        md5 = hashlib.md5(dati).hexdigest()
        return md5

    @staticmethod
    def formatString(string, lenght):
        return string.rjust(lenght)
