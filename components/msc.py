from components.hlr_auc import HLR
from components.vlr import VLR, VLR_data, Call_data

class MSC:
    def __init__(self, name):
        self.name = name
        self.hlr = HLR()
        self.vlr = VLR()
        self.eir = {}

    def add_bsc(self, bsc):
        self.bsc_list.append(bsc)
    
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
                self.vlr.update_call_data(make_call_phone, phone, received_number)
                self.vlr.update_call_data(received_phone, phone, received_number)
                received_phone.bsc.call_confirm(received_phone.bts, received_phone.ms, received_phone.call_data)
                make_call_phone.bsc.call_confirm(make_call_phone.bts, make_call_phone.ms, make_call_phone.call_data)
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
        phone_end_call.bsc.end_call(phone_end_call.bts, phone_end_call.ms, phone_end_call.call_data)
        phone_receive_end_call.bsc.end_call(phone_receive_end_call.bts, phone_receive_end_call.ms, phone_end_call.call_data)
        return True
        
    