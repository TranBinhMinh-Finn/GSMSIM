from random import randint
from bsc import BSC
from bts import BTS
from phone import Phone
from datetime import datetime

TMSI_GEN_RANGE = 2 ** 32 - 2

class Call_data:
    number_make_call: str
    number_receive_call: str
    start_time: datetime

class VLR_data:
    imsi: int
    tmsi: int
    is_busy: bool
    call_data: Call_data
    bsc: BSC 
    bts: BTS
    ms: Phone
    
class VLR:
    def __init__(self):
        self.ms_db = {}
        self.assigned_tmsi=[]
        
    def search_phone(self, phone):
        return self.ms_db[phone]
        
    def change_status(self, phone):
        self.ms_db[phone].is_busy = 1 - self.ms_db[phone].is_busy
    
    def update_call_data(self, phone, make_call_number, received_call_number):
        self.ms_db[phone].call_data = Call_data(make_call_number, received_call_number, None)
    
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
        