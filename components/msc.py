from .hlr_auc import HLR
from .vlr import VLR, VLR_data

class MSC:
    def __init__(self, name="", hlr = None):
        self.name = name
        self.hlr = hlr
        self.vlr = VLR()
        self.eir = {}

    def add_bsc(self, bsc):
        self.bsc_list.append(bsc)
    
    #TODO: make an add bts function. Add bts to an available bsc. If all bsc are at capacity, create a new one.
    def authenticate(self, phone):
        RAND, Kc, SRES = self.hlr.create_triplet(phone.number)
        if RAND == -1:
            #TODO: check hlr of other networks
            return False
        if SRES == phone.cal_SRES(RAND): # phone authenticate sucessfully
            # assign tmsi
            phone.tmsi = self.vlr.generate_tmsi()
            self.vlr.add_ms(phone.number, VLR_data(phone.imsi, phone.tmsi, False))
            self.hlr.update_vlr(phone.number, self.vlr)
            return True
        return False

    def make_call(self, phone, received_number):
        received_phone = self.vlr.search_phone(received_number)
        make_call_phone = self.vlr.search_phone(phone)
        if received_phone == None or make_call_phone == None: 
            #TODO: Can't find phone number in current vlr
            return False
        else:
            if received_phone.is_busy == False and make_call_phone.is_busy == False:
                #Call successful
                self.vlr.change_status(phone)
                self.vlr.change_status(received_number)
                self.vlr.assign_number_call(make_call_phone, received_number)
                self.vlr.assign_number_call(received_phone, phone)
                received_phone.bsc.call_confirm(received_phone.bts, received_phone.ms, phone)
                make_call_phone.bsc.call_confirm(make_call_phone.bts, make_call_phone.ms, received_number)
            else:
                return False
            return True
    
    def request_end_call(self, phone):
        phone_end_call = self.vlr.search_phone(phone)
        if(phone_end_call.is_busy == False):
            return False
        receive_number = phone_end_call.number_call 
        phone_receive_end_call = self.vlr.search_phone(receive_number)
        self.vlr.change_status(phone)
        self.vlr.change_status(receive_number)
        phone_end_call.bsc.end_call(phone_end_call.bts, phone_end_call.ms)
        phone_receive_end_call.bsc.end_call(phone_receive_end_call.bts, phone_receive_end_call.ms)
        return True
        
    