class Download:

    def __init__(self, sessionId, md5file):
        self.set_sessionId = sessionId
        self.set_md5file = md5file

    def get_sessionId(self):
        return self.sessionId

    def get_md5file(self):
        return self.md5file

    def set_sessionId(self, sessionId):
        self.sessionId = sessionId

    def set_md5file(self, md5file):
        self.md5file = md5file