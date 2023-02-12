
class Phone:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.bts = None

    def connect_to_bts(self, bts):
        if bts.add_phone(self):
            self.bts = bts

    def call(self, number):
        self.bts.bsc.make_call(self, number)

    def text(self, number, message):
        self.bts.bsc.send_sms(self, number, message)