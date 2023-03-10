from components.hlr_auc import HLR
from components.vlr import VLR, VLR_data, Call_data
from .bsc import BSC
from utils import network_db
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
        mcc = phone.imsi[:3]
        mnc = phone.imsi[3:5]
            
        #print(RAND, Kc, SRES)
        if mcc != self.hlr.mcc or mnc != self.hlr.mnc:
            #TODO: check hlr of other networks
            current_hlr = network_db[(mcc, mnc)]
            RAND, Kc, SRES = current_hlr.create_triplet(phone.number)
        else : 
            # phone in current hlr
            current_hlr = self.hlr
            RAND, Kc, SRES = current_hlr.create_triplet(phone.number)
            
        if SRES == phone.cal_SRES(RAND): # phone authenticate sucessfully
            # assign tmsi
            phone.tmsi = self.vlr.generate_tmsi()
            self.vlr.add_ms(phone.number, VLR_data(imsi = phone.imsi, tmsi = phone.tmsi, ms = phone))
            current_hlr.update_vlr(phone.number, self.vlr)
            return True
        return False

    def make_call(self, calling_number, receiving_number):
        receiving_phone = self.vlr.search_phone(receiving_number)
        calling_phone = self.vlr.search_phone(calling_number)
        if receiving_phone == None: # Can't find phone number in current vlr
            #Search phone number in other hlr
            for hlr in network_db:
                if hlr.ms_db[receiving_number] != None:
                    receiving_vlr = hlr.ms_db[receiving_number].serving_vlr
                    receiving_phone = receiving_vlr.search_phone(receiving_number)
                    break
            if receiving_phone == None: # Can't find phone in other hlr
                return 2
        else:
            receiving_vlr = self.vlr
        if receiving_phone.is_busy == False and calling_phone.is_busy == False:
            #Call successful
            if receiving_phone.ms.bts.bsc.call_confirm(receiving_phone.ms.bts, receiving_phone.ms, calling_number) == True:
                self.vlr.change_status(calling_number)
                receiving_vlr.change_status(receiving_number)
                self.vlr.update_call_data(calling_number, receiving_number)
                receiving_vlr.update_call_data(receiving_number, calling_number)
                receiving_phone.ms.bts.bsc.call_connect(receiving_phone.ms.bts, receiving_phone.ms, receiving_phone.call_data)
                calling_phone.ms.bts.bsc.call_connect(calling_phone.ms.bts, calling_phone.ms, calling_phone.call_data)
            else: 
                return 1
        else:
            return 1
        return 0
    
    def request_end_call(self, phone_number):
        phone_end_call = self.vlr.search_phone(phone_number)
        if(phone_end_call.is_busy == False):
            return False
        receive_number = phone_end_call.call_data.number_make_call
        if receive_number == phone_number:
            receive_number = phone_end_call.call_data.number_receive_call
        phone_receive_end_call = self.vlr.search_phone(receive_number)
        receive_vlr = self.vlr
        if phone_receive_end_call == None: # Can't find phone in current vlr
            for hlr in network_db: # Search phone in other hlr
                if hlr.ms_db[receive_number] != None:
                    receiving_vlr = hlr.ms_db[receive_number].serving_vlr
                    phone_receive_end_call = receiving_vlr.search_phone(receive_number)
                    break
            if phone_receive_end_call == None: # Can't find phone in other hlr
                return False
        if phone_receive_end_call.is_busy == False:
            return False
        self.vlr.change_status(phone_number)
        receive_vlr.change_status(receive_number)
        phone_end_call.ms.bts.bsc.end_call(phone_end_call.ms.bts, phone_end_call.ms, phone_end_call.call_data)
        phone_receive_end_call.ms.bts.bsc.end_call(phone_receive_end_call.ms.bts, phone_receive_end_call.ms, phone_receive_end_call.call_data)
        return True
        
    