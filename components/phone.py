from algorithm.com128 import auth

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
            self.bts = bts
            return True
        return False

    def authenticate(self):
        if self.bts.authenticate(self):
            """
            Send a request to authenticate phone with network  
            """
            return True
        else:
            print(f"Authentication failed for {self.name}")
            return False

    def cal_SRES(self, RAND):
        """
        Calculate SRES for challenge
        """
        SRES, Kc = auth(self.Ki, RAND)
        return SRES

    def call(self, number):
        if not self.bts:
            if not self.connect_to_bts(self.search_for_bts()):
                print(f"Failed to connect to network for {self.name}")
                return
        self.bts.make_call(self, number) 
    
    def text(self, number, message):
        if not self.bts:
            if not self.connect_to_bts():
                print(f"Failed to connect to network for {self.name}")
                return
            self.bts.send_sms(self, number, message)