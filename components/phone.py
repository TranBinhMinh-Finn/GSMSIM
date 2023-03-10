from algorithm.com128 import auth
from datetime import datetime

class Phone:
    def __init__(self, number, imsi, ki, name=""):
        self.number = number
        self.name = name
        self.bts = None
        self.ki = ki
        self.kc = None
        self.lai = None
        self.imsi = imsi
        self.tmsi = None

    def search_for_bts(self):
        bts = None
        # find an available bts from a list of bts
        return bts
    
    def connect_to_bts(self, bts):
        if bts.authenticate(self):
            print(f'Phone {self.number} authenticated successful')
            self.bts = bts
            return True
        print(f'Phone {self.number} authenticated failed')
        return False

    def authenticate(self):
        if self.bts.authenticate(self):
            """
            Send a request to authenticate phone with network  
            """
            return True
        else:
            print(f"Authentication failed for {self.number}")
            return False

    def cal_SRES(self, RAND):
        """
        Calculate SRES for challenge
        """
        Kc, SRES = auth(self.ki, RAND)
        return SRES

    def make_call(self, receiving_number):
        if not self.bts:
            if not self.connect_to_bts(self.search_for_bts()):
                print(f"Failed to connect to network for {self.number}")
                return
        result = self.bts.make_call(self.number, receiving_number)
        if result == 1:
            print(f"{self.number}: Receiver is busy")
        if result == 2: 
            print(f"{self.number}: Receiver doesn't exist")
    
    def call_confirm(self, call_data):
        number_call = call_data.number_make_call
        if self.number == number_call:
            number_call = call_data.number_receive_call
        print(f"{self.number}: Call started with number: {number_call}")
    
    def request_end_call(self):
        result = self.bts.request_end_call(self.number)
        if result == True:
            print(f"End successful from {self.number}")
        else:
            print(f"Fail to end call from {self.number}")
    
    def end_call(self, call_data):
        number_call = call_data.number_make_call
        end_time = datetime.now()
        if number_call == self.number:
            number_call = call_data.number_receive_call
        print(f"{self.number}: Call with number {number_call} ended in {end_time - call_data.start_time}")
    
    def text(self, number, message):
        if not self.bts:
            if not self.connect_to_bts():
                print(f"Failed to connect to network for {self.name}")
                return
            self.bts.send_sms(self, number, message)