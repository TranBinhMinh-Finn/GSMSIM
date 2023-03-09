
class BTS:
    def __init__(self, bsc, name = "bts"):
        self.name = name
        self.bsc = bsc
        
    def authenticate(self, phone):
        """
        Pass the authentication request to BSC
        """
        return self.bsc.authenticate(phone)
        
    def make_call(self, calling_number, receiving_number):
        return self.bsc.make_call(calling_number, receiving_number)
        
    def call_confirm(self, phone, call_data):
        phone.call_confirm(call_data)
        
    def request_end_call(self, phone_number):
        return self.bsc.request_end_call(phone_number)
    
    def end_call(self, phone, call_data):
        phone.end_call(call_data)
    
    def send_sms(self, phone, number, message):
        self.bsc.send_sms(phone, number, message)
