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

    def call_confirm(self, bts, phone, from_number):
        bts.call_confirm(phone, from_number)
        
    def request_end_call(self, phone_number):
        return self.msc.request_end_call(phone_number)
    
    def end_call(self, bts, phone):
        bts.end_call(phone)
    
    def send_sms(self, phone, number, message):
        recipient = self.msc.search_phone(number)
        if recipient:
            print(f"SMS from {phone.name} to {recipient.name} ({recipient.number}): {message}")
        else:
            print(f"Phone number {number} not found.")
            
    def authenticate(self, phone):
        """
        Pass the authentication request to MSC
        """
        return self.msc.authenticate(phone)