class BSC:
    def __init__(self, msc, name):
        self.msc = msc
        self.name = name
        self.bts_list = []

    def add_bts(self, bts):
        self.bts_list.append(bts)

    def make_call(self, phone, number):
        recipient = self.msc.search_phone(number)
        if recipient:
            print(f"Call from {phone.name} to {recipient.name} ({recipient.number})")
        else:
            print(f"Phone number {number} not found.")

    def send_sms(self, phone, number, message):
        recipient = self.msc.search_phone(number)
        if recipient:
            print(f"SMS from {phone.name} to {recipient.name} ({recipient.number}): {message}")
        else:
            print(f"Phone number {number} not found.")