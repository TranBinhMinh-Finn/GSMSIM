from random import randint
from algorithm.com128 import auth

class HLR:
    def __init__(self):
        self.ms_db = {}
    
    def search_Ki(self, imsi):
        return self.ms_db[imsi]
    
    def create_triplet(self, imsi):
        Ki = self.search_Ki(imsi)
        if Ki == None:
            return -1
        RAND = randint(0, 65535)
        Kc, SRES = auth(Ki, RAND)
        return RAND, Kc, SRES