
class BTS:
    def __init__(self, bsc, name = "bts"):
        self.name = name
        self.bsc = bsc
        self.phones = []
        
    def authenticate(self, phone):
        """
        Pass the authentication request to BSC
        """
        self.bsc.authenticate(phone)
        
    def make_call(self, phone, number):
        self.bsc.make_call(phone, number)
        
    def send_sms(self, phone, number, message):
        self.bsc.send_sms(phone, number, message)
