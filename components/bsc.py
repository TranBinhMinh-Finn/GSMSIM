from .vlr import Call_data

from .bts import BTS
BSC_CAPACITY = 5

class BSC:
    def __init__(self, msc, name="bsc", capacity=BSC_CAPACITY):
        self.msc = msc
        self.name = name
        self.capacity = capacity
        self.bts_list = []

    def add_bts(self):
        if len(self.bts_list) == self.capacity:
            return None
        self.bts_list.append(BTS(bsc = self))
        return self.bts_list[-1]
    
    def make_call(self, calling_number, receiving_number):
        return self.msc.make_call(calling_number, receiving_number)

    def call_connect(self, bts, phone, call_data):
        bts.call_connect(phone, call_data)
        
    def call_alert(self, phone_number):
        return self.msc.call_alert(phone_number)
    
    def call_confirm(self, first_number, second_number, confirm):
        self.msc.call_confirm(first_number, second_number, confirm)
    
    def request_end_call(self, phone_number):
        return self.msc.request_end_call(phone_number)
    
    def end_call(self, bts, phone, call_data):
        bts.end_call(phone, call_data)
    
    def send_sms(self, phone, number, message):
        recipient = self.msc.search_phone(number)
        if recipient:
            print(f"SMS from {phone.name} to {recipient.name} ({recipient.number}): {message}")
        else:
            print(f"Phone number {number} not found.")
            
    def handle_connection_request(self, phone):
        """
        Pass the connection request to MSC
        """
        return self.msc.authenticate(phone)