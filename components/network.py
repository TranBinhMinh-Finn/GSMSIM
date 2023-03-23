import os,binascii
from .msc import MSC
from .hlr_auc import HLR, HLR_data
from .phone import Phone
from utils import networks, network_code_mappings

class Network:
   
    def __init__(self, mcc, mnc, cc, ndc) -> None:
        self.mcc = mcc # mobile country code
        self.mnc = mnc # mobile network code
        self.cc = cc # country code
        self.ndc = ndc # national destination code
        self.hlr = HLR(self, mcc, mnc, cc, ndc)
        self.msc = MSC(hlr=self.hlr)
        self.ms_list = {}
        self.ms_count = 0
        self.bts_count = 0
        self.bsc_count = 0
        networks[(mcc, mnc)] = self
        network_code_mappings[(cc, ndc)] = (mcc, mnc)
        
    def add_bts(self):
        self.bts_count += 1
        result = self.msc.add_bts()
        if result == False:
            self.bsc_count += 1
    
    def get_available_bts(self):
        return self.msc.get_available_bts()
        
    def create_new_ms(self):
        self.ms_count+=1
        phone_number = self.cc + self.ndc + format(self.ms_count,"010d")
        imsi = self.mcc + self.mnc + format(self.ms_count,"010d")
        Ki = binascii.b2a_hex(os.urandom(16)).decode("utf-8")
        self.ms_list[phone_number] = Phone(number=phone_number, imsi=imsi, ki=Ki)
        self.hlr.add_ms(phone_number=phone_number, data=HLR_data(imsi=imsi, Ki=Ki))
        return Phone(
                    number=phone_number,
                    imsi=imsi,
                    ki=Ki)
    
    def show_number_bts_bsc(self):
        print(f"There are {self.bts_count} bts in this network")
        print(f"There are {self.bsc_count} bsc in this network")
    
    def show_all_ms(self):
        print(f"There are {self.ms_count} ms in this network.")
        for phone in self.ms_list:
            print(phone)
            
    def show_ms_info(self, number):
        phone = self.ms_list.get(number)
        if phone != None:
            print(f"Phone number: {phone.number}")
            print(f"IMSI: {phone.imsi}")
            print(f"Ki: {phone.ki}")
        else:
            print(f"Can't find this phone number current nerwork")
    
        