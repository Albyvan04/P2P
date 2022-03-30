class Log:
    def __init__(self, sessionID, tipo_operazione, data, ora):
        self.sessionID = sessionID
        self.tipo_operazione = {'LOGI':'Login', 'ADDF':'Aggiunta', 'DELF':'Rimozione', 'FIND':'Ricerca', 'RETR':'Download', 'LOGO':'Logout'}
        self.data = data
        self.ora = ora

    