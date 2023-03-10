from random import randint
from .phone import Phone
from datetime import datetime

TMSI_GEN_RANGE = 2 ** 32 - 2

class Call_data:
    def __init__(self, number_make_call, number_receive_call, start_time):
        self.number_make_call = number_make_call
        self.number_receive_call = number_receive_call
        self.start_time = start_time
    number_make_call: str
    number_receive_call: str
    start_time: datetime

class VLR_data:
    def __init__(self, imsi, tmsi, ms):
        self.imsi = imsi
        self.tmsi = tmsi
        self.ms = ms
        self.is_busy = False
        self.phone_calling = None
        self.call_data = None
    imsi: int
    tmsi: int
    is_busy: bool
    call_data: Call_data
    ms: Phone
    
class VLR:
    def __init__(self):
        self.ms_db = {}
        self.assigned_tmsi=[]
        
    def search_phone(self, phone_number):
        return self.ms_db[phone_number]
        
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
        