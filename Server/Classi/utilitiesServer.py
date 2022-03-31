import random
import string

class Utilities:

    @staticmethod
    def generateSessionID():
        sessionID = ''
        i = 0

        while i < 16:
            tmp = random.randint(0,1)
            if(tmp == 0):
                letters = string.ascii_uppercase
                sessionID += random.choice(letters)
            else:
                letters = string.digits
                sessionID += random.choice(letters)
            i += 1
        return sessionID
