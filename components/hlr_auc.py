import os, binascii
from random import randint
from algorithm.com128 import auth
from .vlr import VLR

class HLR_data:
    imsi: int
    serving_vlr: VLR
    Ki: str
    def __init__(self, imsi, Ki, serving_vlr=None):
        self.imsi = imsi
        self.Ki = Ki
        self.serving_vlr = serving_vlr

    
class HLR:
    def __init__(self):
        self.ms_db = {}
    
    def search_Ki(self, phone_number):
        return self.ms_db[phone_number].Ki
    
    def create_triplet(self, phone_number):
        Ki = self.search_Ki(phone_number)
        if Ki == None:
            return -1
        RAND = binascii.b2a_hex(os.urandom(16)).decode("utf-8")  #randint(0, 65535)
        Kc, SRES = auth(Ki, RAND)
        return RAND, Kc, SRES
    
    def add_ms(self, phone_number, data):
        self.ms_db[phone_number] = data
        
    def remove_ms(self, phone_number):
        self.ms_db.pop(phone_number)
        
    def update_vlr(self, phone_number, vlr):
        self.ms_db[phone_number].vlr = vlr
