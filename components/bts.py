
class BTS:
    def __init__(self, bsc, name = "bts"):
        self.name = name
        self.bsc = bsc
        
    def authenticate(self, phone):
        """
        Pass the authentication request to BSC
        """
        self.bsc.authenticate(phone)
        
    def make_call(self, phone, received_number):
        return self.bsc.make_call(phone, received_number)
        
    def call_confirm(self, phone, from_number):
        phone.call_confirm(from_number)
        
    def request_end_call(self, phone):
        return self.bsc.end_call(phone)
    
    def end_call(self, phone):
        phone.end_call()
    
    def send_sms(self, phone, number, message):
        self.bsc.send_sms(phone, number, message)
