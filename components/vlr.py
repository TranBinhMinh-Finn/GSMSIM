from random import randint
from .phone import Phone
from datetime import datetime

TMSI_GEN_RANGE = 2 ** 32 - 2

class Call_data:
    def __init__(self, first_number, second_number, start_time):
        self.first_number = first_number
        self.second_number = second_number
        self.start_time = start_time
    

class VLR_data:
    def __init__(self, imsi, tmsi, ms, lai):
        self.imsi = imsi
        self.tmsi = tmsi
        self.ms = ms
        self.is_busy = False
        self.phone_calling = None
        self.call_data = None
        self.lai = lai
    imsi: int
    tmsi: int
    is_busy: bool
    call_data: Call_data
    phone_calling: str
    ms: Phone
    
class VLR:
    def __init__(self, msc):
        self.msc = msc
        self.ms_db = {}
        self.assigned_tmsi=[]
        
    def search_phone(self, phone_number):
        return self.ms_db.get(phone_number)
        
    def change_status(self, phone_number):
        self.ms_db[phone_number].is_busy = 1 - self.ms_db[phone_number].is_busy

    def update_call_data(self, first_number, second_number):
        current_time = datetime.now()
        self.ms_db[first_number].call_data = Call_data(first_number, second_number, current_time)
    
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
        