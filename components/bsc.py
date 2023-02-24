from vlr import Call_data

BSC_CAPACITY = 5
class BSC:
    def __init__(self, msc, name, capacity=BSC_CAPACITY):
        self.msc = msc
        self.name = name
        self.capacity = capacity

    def add_bts(self, bts):
        self.bts_list.append(bts)

    def make_call(self, phone, received_number):
        return self.msc.make_call(phone, received_number)

    def call_confirm(self, bts, phone, from_number):
        bts.call_confirm(phone, from_number)
        
    def request_end_call(self, phone):
        return self.msc.request_end_call(phone)
    
    def end_call(self, bts, phone, call_data):
        bts.end_call(phone, call_data)
    
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
        self.msc.authenticate(phone)