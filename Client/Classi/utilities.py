from fileinput import filename
import hashlib
import re

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
    def formatPort(port):
        return '%05d' % int(port)


    @staticmethod
    def get_md5 (fileName):
        file = open("sharedFiles/"+ fileName, 'rb')
        dati = file.read()
        md5 = ''
        md5 = hashlib.md5(dati).hexdigest()
        return md5

    @staticmethod
    def formatString(string, lenght):
        return string.rjust(lenght, '|')