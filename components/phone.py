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

    def connect_to_bts(self, bts):
        self.bts = bts

    def authenticate(self):
        if self.bts.bsc.msc.authenticate(self.imsi):
            return True
        else:
            print(f"Authentication failed for {self.name}")
            return False

    def cal_SRES(self, RAND):
        SRES, Kc = auth(self.Ki, RAND)
        return SRES

    def call(self, number):
        if self.authenticate():
            self.bts.bsc.make_call(self, number) 
    
    def text(self, number, message):
        if self.authenticate():
            self.bts.bsc.send_sms(self, number, message)