from components.hlr_auc import HLR
from components.vlr import VLR, VLR_data, Call_data
from .bsc import BSC
class MSC:
    def __init__(self, name="", hlr = None):
        self.name = name
        self.hlr = hlr
        self.vlr = VLR()
        self.eir = {}
        self.bsc_list = []

    def add_bsc(self):
        self.bsc_list.append(BSC(msc=self))
    
    def add_bts(self):
        for bsc in self.bsc_list:
            if bsc.add_bts():
                return
        self.add_bsc()
        self.bsc_list[-1].add_bts()
        
    def authenticate(self, phone):
        RAND, Kc, SRES = self.hlr.create_triplet(phone.number)
        print(RAND, Kc, SRES)
        if RAND == -1:
            #TODO: check hlr of other networks
            return False
        if SRES == phone.cal_SRES(RAND): # phone authenticate sucessfully
            # assign tmsi
            phone.tmsi = self.vlr.generate_tmsi()
            self.vlr.add_ms(phone.number, VLR_data(imsi = phone.imsi, tmsi = phone.tmsi, ms = phone))
            self.hlr.update_vlr(phone.number, self.vlr)
            return True
        return False

    def make_call(self, calling_number, receiving_number):
        receiving_phone = self.vlr.search_phone(receiving_number)
        calling_phone = self.vlr.search_phone(calling_number)
        if receiving_phone == None or calling_phone == None: 
            #TODO: Can't find phone number in current vlr
            return False
        else:
            if receiving_phone.is_busy == False and calling_phone.is_busy == False:
                #Call successful
                self.vlr.change_status(calling_number)
                self.vlr.change_status(receiving_number)
                self.vlr.assign_number_call(calling_number, receiving_number)
                self.vlr.assign_number_call(receiving_number, calling_number)
                receiving_phone.ms.bts.bsc.call_confirm(receiving_phone.ms.bts, receiving_phone.ms, calling_number)
                calling_phone.ms.bts.bsc.call_confirm(calling_phone.ms.bts, calling_phone.ms, receiving_number)
            else:
                return False
            return True
    
    def request_end_call(self, phone_number):
        phone_end_call = self.vlr.search_phone(phone_number)
        if(phone_end_call.is_busy == False):
            return False
        receive_number = phone_end_call.number_call 
        phone_receive_end_call = self.vlr.search_phone(receive_number)
        self.vlr.change_status(phone_number)
        self.vlr.change_status(receive_number)
        phone_end_call.ms.bts.bsc.end_call(phone_end_call.ms.bts, phone_end_call.ms)
        phone_receive_end_call.ms.bts.bsc.end_call(phone_receive_end_call.ms.bts, phone_receive_end_call.ms)
        return True
        
    