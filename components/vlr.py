from random import randint

TMSI_GEN_RANGE = 2 ** 32 - 2


class VLR:
    def __init__(self, hlr):
        self.hlr = hlr
        self.ms_db = {}
        self.assigned_tmsi=[]
        
    def generate_tmsi(self):
        tmsi = randint(0, TMSI_GEN_RANGE)
        while tmsi in self.assigned_tmsi:
            tmsi = randint(0, TMSI_GEN_RANGE)
        self.assigned_tmsi.append(tmsi)
        return tmsi