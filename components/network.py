import os,binascii
from .msc import MSC
from .hlr_auc import HLR, HLR_data
from .phone import Phone
from utils import network_db, network_code_mappings

class Network:
   
    def __init__(self, mcc, mnc, cc, ndc) -> None:
        self.mcc = mcc # mobile country code
        self.mnc = mnc # mobile network code
        self.cc = cc # country code
        self.ndc = ndc # national destination code
        self.hlr = HLR(mcc, mnc, cc, ndc)
        self.msc = MSC(hlr=self.hlr)
        self.ms_count = 0
        network_db[(mcc, mnc)] = self.hlr
        network_code_mappings[(cc, ndc)] = (mcc, mnc)
        
    def add_bts(self):
        return self.msc.add_bts()
        
    def create_new_ms(self):
        self.ms_count+=1
        phone_number = self.cc + self.ndc + format(self.ms_count,"010d")
        imsi = self.mcc + self.mnc + format(self.ms_count,"010d")
        Ki = binascii.b2a_hex(os.urandom(16)).decode("utf-8") 
        self.hlr.add_ms(phone_number=phone_number, data=HLR_data(imsi=imsi, Ki=Ki))
        return Phone(
                    number=phone_number,
                    imsi=imsi,
                    ki=Ki)
        
    
        