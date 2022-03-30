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