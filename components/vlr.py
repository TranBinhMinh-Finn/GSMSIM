from random import randint

TMSI_GEN_RANGE = 2 ** 32 - 2


class VLR_data:
    imsi: int
    tmsi: int
    is_busy: bool
     
    
class VLR:
    def __init__(self):
        self.ms_db = {}
        self.assigned_tmsi=[]
        
    def generate_tmsi(self):
        tmsi = randint(0, TMSI_GEN_RANGE)
        while tmsi in self.assigned_tmsi:
            tmsi = randint(0, TMSI_GEN_RANGE)
        self.assigned_tmsi.append(tmsi)
        return tmsi
    
    def add_ms(self, phone_number, data):
        self.ms_db[phone_number] = data
        
    def remove_ms(self, phone_number):
        self.assigned_tmsi.remove(self.ms_db[phone_number].tmsi)
        self.ms_db.pop(phone_number)
        