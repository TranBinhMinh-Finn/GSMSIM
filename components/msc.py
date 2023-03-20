from components.hlr_auc import HLR
from components.vlr import VLR, VLR_data, Call_data
from .bsc import BSC
import os,binascii
from utils import network_db, network_code_mappings
class MSC:
    def __init__(self, name="", hlr = None):
        self.name = name
        self.hlr = hlr
        self.vlr = VLR()
        self.eir = {}
        self.bsc_list = {}

    def add_bsc(self):
        while True:
            lac = binascii.b2a_hex(os.urandom(2)).decode("utf-8")
            if lac not in self.bsc_list.keys() and lac!= 'ffff':
                break  
        self.bsc_list[lac] = BSC(msc=self, lac=lac)
        return self.bsc_list[lac]
    
    def add_bts(self):
        for bsc in self.bsc_list.values():
            if bsc.add_bts():
                return
        self.add_bsc().add_bts()
        
    def authenticate(self, bsc, bts, phone):
        """
        Authenticate the requesting MS and update the vlr if successful
        """
        mcc = phone.imsi[:3]
        mnc = phone.imsi[3:5]
            
        if mcc != self.hlr.mcc or mnc != self.hlr.mnc:
            current_hlr = network_db[(mcc, mnc)]
            RAND, Kc, SRES = current_hlr.create_triplet(phone.number)
        else : 
            # phone in current hlr
            current_hlr = self.hlr
            RAND, Kc, SRES = current_hlr.create_triplet(phone.number)
            
        if SRES == bsc.auth_challenge(bts, phone, RAND): # phone authenticate sucessfully
            # assign tmsi
            phone.tmsi = self.vlr.generate_tmsi()
            phone.lai = self.hlr.mcc + self.hlr.mnc + bsc.lac
            self.vlr.add_ms(phone.number, VLR_data(imsi=phone.imsi, tmsi=phone.tmsi, ms=phone))
            current_hlr.update_vlr(phone.number, self.vlr)
            return True
        return False

    def find_vlr_data(self, number):
        if len(number) >= 4:
            cc = number[:2]
            ndc = number[2:4]
            network_code =  network_code_mappings.get((cc, ndc))
            if network_code != None:
                hlr = network_db.get(network_code)
                if hlr != None:
                    if hlr.search_phone(number) != None:
                        vlr = hlr.ms_db[number].serving_vlr
                        phone = vlr.search_phone(number)
                        if phone != None: 
                            return (vlr, phone)
        return (None, None) # Can't find phone in other hlr

    def make_call(self, calling_number, receiving_number):
        # get phone data of both numbers 
        (receiving_vlr, receiving_phone) = self.find_vlr_data(receiving_number)
        calling_phone = self.vlr.search_phone(calling_number)
        if receiving_phone == None: # Can't find receive phone number
            return 2
        if receiving_phone.is_busy == False and calling_phone.is_busy == False:
            self.vlr.change_status(calling_number)
            receiving_vlr.change_status(receiving_number)
            receiving_phone.phone_calling = calling_number
            receiving_phone.ms.bts.bsc.call_alert(receiving_phone.ms, receiving_phone.ms.bts , calling_number)
            return 0
            #Call successful
        else:
            return 1 # Receiver is busy
    
    def call_confirm(self, first_number, second_number, confirm):
        first_vlr, first_phone = self.find_vlr_data(first_number)
        second_vlr, second_phone = self.find_vlr_data(second_number)
        if confirm == True:
            first_vlr.update_call_data(first_number, second_number, first_vlr, second_vlr)
            second_vlr.update_call_data(second_number, first_number, second_vlr, first_vlr)
            second_phone.ms.bts.bsc.call_connect(second_phone.ms.bts, second_phone.ms, second_phone.call_data)
            first_phone.ms.bts.bsc.call_connect(first_phone.ms.bts, first_phone.ms, first_phone.call_data)
        else: 
            second_phone.ms.bts.bsc.call_decline(second_phone.ms.bts, second_phone.ms)
            first_vlr.change_status(first_number)
            second_vlr.change_status(second_number)
    
    def request_end_call(self, first_number, second_number, in_call):
        first_ms = self.vlr.search_phone(first_number)
        if first_ms.is_busy == False:
            return False
        second_vlr, second_ms = self.find_vlr_data(second_number)
        if in_call == False:
            self.vlr.change_status(first_number)
            second_vlr.change_status(second_number)
            second_ms.phone_calling = None
            return True
        second_ms = second_vlr.search_phone(second_number)
        if second_ms == None: # Can't find phone in current vlr
            self.vlr.change_status(first_number)
        if second_ms.is_busy == False:
            return False
        self.vlr.change_status(first_number)
        second_vlr.change_status(second_number)
        first_ms.ms.bts.bsc.end_call(first_ms.ms.bts, first_ms.ms, first_ms.call_data)
        second_ms.ms.bts.bsc.end_call(second_ms.ms.bts, second_ms.ms, second_ms.call_data)
        return True
        
    