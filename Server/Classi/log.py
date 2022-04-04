class Log:
    def __init__(self, ID, sessionID, tipo_operazione, data, ora):
        self.ID = ID
        self.sessionID = sessionID
        self.tipo_operazione = {'LOGI':'Login', 'ADDF':'Aggiunta', 'DELF':'Rimozione', 'FIND':'Ricerca', 'RETR':'Download', 'LOGO':'Logout'}
        self.data = data
        self.ora = ora