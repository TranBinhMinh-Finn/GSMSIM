from .vlr import Call_data

from .bts import BTS
BSC_CAPACITY = 5

class BSC:
    def __init__(self, msc, lac, name="bsc", capacity=BSC_CAPACITY):
        self.msc = msc
        self.name = name
        self.capacity = capacity
        self.bts_list = []
        self.lac = lac # location area code
        self.ms_route = {}
        
    def add_bts(self):
        if len(self.bts_list) == self.capacity:
            return None
        self.bts_list.append(BTS(bsc = self))
        return self.bts_list[-1]
    
    def make_call(self, calling_number, receiving_number):
        return self.msc.make_call(calling_number, receiving_number)

    def call_connect(self, tmsi, call_data):
        bts = self.ms_route.get(tmsi)
        bts.call_connect(tmsi, call_data)
    
    def call_decline(self, tmsi):
        bts = self.ms_route.get(tmsi)
        bts.call_decline(tmsi)
        
    def call_alert(self, tmsi, from_number):
        bts = self.ms_route.get(tmsi)
        return bts.call_alert(tmsi, from_number)
    
    def call_confirm(self, first_number, second_number, confirm):
        self.msc.call_confirm(first_number, second_number, confirm)
    
    def request_end_call(self, first_number, second_number, in_call):
        return self.msc.request_end_call(first_number, second_number, in_call)
    
    def end_call(self, tmsi):
        bts = self.ms_route.get(tmsi)
        bts.end_call(tmsi)
    
    def send_sms(self, sending_number, receiving_number, message):
        self.msc.send_sms(sending_number, receiving_number, message)
        
    def receive_sms(self, sending_number, receiving_tmsi, message):
        bts = self.ms_route.get(receiving_tmsi)    
        bts.receive_sms(sending_number, message, receiving_tmsi)       

    def handle_connection_request(self, bts, phone):
        """
        Pass the connection request to MSC
        """
        if self.msc.authenticate(self, bts, phone):
            self.ms_route[phone.tmsi] = bts
            return True
        return False
    
    def auth_challenge(self, bts, phone, RAND):
        return bts.auth_challenge(phone, RAND)