from algorithm.com128 import auth

class Phone:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.bts = None
        self.rand = None
        self.Ki = None

    def connect_to_bts(self, bts):
        if bts.add_phone(self):
            self.bts = bts
            self.bts.bsc.msc.vlr.white.append(self)

    def cal_SRES(self, RAND):
        if(self.rand == None):
            self.rand = RAND
        SRES, Kc = auth(self.Ki, RAND)
        return SRES

    def call(self, number):
        if(self.bts.bsc.msc.vlr.auth_check(self)):
            self.bts.bsc.make_call(self, number)
            return True
        return False

    def text(self, number, message):
        self.bts.bsc.send_sms(self, number, message)