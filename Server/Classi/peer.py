class Peer:

    def __init__(self, session_id, ip, port):
        self.set_session_id(session_id)
        self.set_ip(ip)
        self.set_port(port)

    def set_session_id(self, sid):
        self.__session_id = sid

    def set_ip(self, ip):
        self.__ip = ip
    
    def set_port(self, port):
        self.__port = port

    def get_session_id(self):
        return self.__session_id

    def get_ip(self):
        return self.__ip

    def get_port(self):
        return self.__port
    
        
