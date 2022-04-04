class Download:
    __init__(self, sessionId, md5file):
        self.set_sessionId = sessionId
        self.set_md5file = md5file

    get_sessionId(self):
        return self.sessionId

    get_md5file(self):
        return self.md5file

    set_sessionId(self, sessionId):
        self.sessionId = sessionId

    set_md5file(self, md5file):
        self.md5file = md5file