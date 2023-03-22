from components.hlr_auc import HLR
from components.vlr import VLR, VLR_data, Call_data
from .bsc import BSC
import os,binascii
from utils import networks, network_code_mappings
class MSC:
    def __init__(self, hlr):
        self.hlr = hlr
        self.vlr = VLR(msc=self)
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
    
    def get_available_bts(self):
        for bsc in self.bsc_list.values():
            for bts in bsc.bts_list:
                if len(bts.ms_list.values()) < bts.capacity:
                    return bts
    
    def authenticate(self, bsc, bts, phone):
        """
        Authenticate the requesting MS and update the vlr if successful
        """
        mcc = phone.imsi[:3]
        mnc = phone.imsi[3:5]
            
        if mcc != self.hlr.mcc or mnc != self.hlr.mnc:
            network = networks[(mcc, mnc)]
            if network is not None:
                current_hlr = network.hlr
            RAND, Kc, SRES = current_hlr.create_triplet(phone.number)
        else : 
            # phone in current hlr
            current_hlr = self.hlr
            RAND, Kc, SRES = current_hlr.create_triplet(phone.number)
            
        if SRES == bsc.auth_challenge(bts, phone, RAND): # phone authenticate sucessfully
            # assign tmsi
            phone.tmsi = self.vlr.generate_tmsi()
            phone.lai = self.hlr.mcc + self.hlr.mnc + bsc.lac
            self.vlr.add_ms(phone.number, VLR_data(imsi=phone.imsi, tmsi=phone.tmsi, ms=phone, lai=phone.lai))
            current_hlr.update_vlr(phone.number, self.vlr)
            return True
        return False

    def find_serving_vlr(self, number):
        if len(number) >= 4:
            cc = number[:2]
            ndc = number[2:4]
            network_code =  network_code_mappings.get((cc, ndc))
            if network_code != None:
                network = networks.get(network_code)
                if network is not None:
                    hlr = network.hlr
                    if hlr.search_phone(number) != None:
                        vlr = hlr.ms_db[number].serving_vlr
                        phone = vlr.search_phone(number)
                        if phone != None: 
                            return (vlr, phone)
        return (None, None) # Can't find phone in other hlr

    def get_serving_bsc(self, phone):
        return self.bsc_list.get(phone.lai[-4:])
        
    def make_call(self, calling_number, receiving_number, flag=False):
        """
        Call setup
        """
        if not flag: # msc on the calling side
            (receiving_vlr, receiving_phone) = self.find_serving_vlr(receiving_number)
            calling_phone = self.vlr.search_phone(calling_number)
            if receiving_phone == None: # Can't find receiving phone number
                return 2
            if receiving_phone.is_busy == False and calling_phone.is_busy == False:
                self.vlr.change_status(calling_number)
                # Call the msc of receiving side to setup the call
                receiving_vlr.msc.make_call(calling_number, receiving_number, flag=True)
                return 0 # Call successful
            else:
                return 1 # Receiver is busy
        else: # msc on the receiving side
            self.vlr.change_status(receiving_number)
            receiving_phone = self.vlr.search_phone(receiving_number)
            receiving_phone.phone_calling = calling_number
            bsc = self.get_serving_bsc(receiving_phone)
            if bsc is not None:
                return bsc.call_alert(receiving_phone.tmsi, calling_number)
            return 1
        
    
    def call_confirm(self, receiving_number, calling_number, confirm, flag=False):
        """
        Handle a confirmation or decline response from receiving phone
        """
        if not flag:
            receiving_phone = self.vlr.search_phone(receiving_number)
            calling_vlr, calling_phone = self.find_serving_vlr(calling_number)
            bsc = self.get_serving_bsc(receiving_phone)
            if confirm == True:
                self.vlr.update_call_data(receiving_number, calling_number)
                bsc.call_connect(receiving_phone.tmsi, receiving_phone.call_data)    
            else:
                self.vlr.change_status(receiving_number) 
            calling_vlr.msc.call_confirm(receiving_number, calling_number, confirm, flag=True)
        else:
            calling_phone = self.vlr.search_phone(calling_number)
            bsc = self.get_serving_bsc(calling_phone)
            if confirm == True:
                self.vlr.update_call_data(calling_number, receiving_number)
                bsc.call_connect(calling_phone.tmsi, calling_phone.call_data)
            else: 
                bsc.call_decline(calling_phone.tmsi)
                self.vlr.change_status(calling_number) 
            
    
    def request_end_call(self, first_number, second_number, in_call, flag=False):
        """
        Handle the request to end call
        """
        if not flag:
            first_ms = self.vlr.search_phone(first_number)
            if first_ms.is_busy == False:
                return False
            self.vlr.change_status(first_number)
            second_vlr, second_ms = self.find_serving_vlr(second_number)
            bsc = self.get_serving_bsc(first_ms)
            bsc.end_call(first_ms.tmsi)
            return second_vlr.msc.request_end_call(first_number, second_number, in_call, flag=True)
        else:
            second_ms = self.vlr.search_phone(second_number)
            if second_ms.is_busy == False:
                return False
            self.vlr.change_status(second_number)
            bsc = self.get_serving_bsc(second_ms)
            bsc.end_call(second_ms.tmsi)
            return True
        
    