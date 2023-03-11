from components.hlr_auc import HLR
from components.vlr import VLR, VLR_data, Call_data
from .bsc import BSC
from utils import network_db, network_code_mappings
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
            self.vlr.add_ms(phone.number, VLR_data(imsi=phone.imsi, tmsi=phone.tmsi, ms=phone))
            current_hlr.update_vlr(phone.number, self.vlr)
            return True
        return False

    def make_call(self, calling_number, receiving_number):
        # get phone data of both numbers 
        receiving_phone = self.vlr.search_phone(receiving_number)
        calling_phone = self.vlr.search_phone(calling_number)
        if receiving_phone == None: # Can't find phone number in current vlr
            # Search the ms in receiving number's hlr
            cc = receiving_number[:2]
            ndc = receiving_number[2:4]
            network_code =  network_code_mappings.get((cc, ndc))
            if network_code == None:
                return 2
            hlr = network_db.get(network_code)
            if hlr == None:
                return 2
            if hlr.search_phone(receiving_number) != None:
                receiving_vlr = hlr.ms_db[receiving_number].serving_vlr
                receiving_phone = receiving_vlr.search_phone(receiving_number)
                if receiving_phone == None: # Can't find phone in other hlr
                    return 2
            else:
                return 2
        else:
            receiving_vlr = self.vlr
        if receiving_phone.is_busy == False and calling_phone.is_busy == False:
            #Call successful
            if receiving_phone.ms.bts.bsc.call_confirm(receiving_phone.ms.bts, receiving_phone.ms, calling_number) == True:
                self.vlr.change_status(calling_number)
                receiving_vlr.change_status(receiving_number)
                self.vlr.update_call_data(calling_number, receiving_number, self.vlr, receiving_vlr)
                receiving_vlr.update_call_data(receiving_number, calling_number, receiving_vlr, self.vlr)
                receiving_phone.ms.bts.bsc.call_connect(receiving_phone.ms.bts, receiving_phone.ms, receiving_phone.call_data)
                calling_phone.ms.bts.bsc.call_connect(calling_phone.ms.bts, calling_phone.ms, calling_phone.call_data)
            else: 
                return 1
        else:
            return 1
        return 0
    
    def request_end_call(self, first_number):
        first_ms = self.vlr.search_phone(first_number)
        if(first_ms.is_busy == False):
            return False
        second_number = first_ms.call_data.second_number
        second_vlr = first_ms.call_data.second_vlr
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
        
    