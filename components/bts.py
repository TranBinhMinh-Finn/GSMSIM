DEFAULT_CAPACITY = 10
DEFAULT_CHANNELS = 1

class BTS:
    def __init__(self, bsc, id="", capacity = DEFAULT_CAPACITY, traffic_channels = DEFAULT_CHANNELS):
        self.id = id
        self.bsc = bsc
        self.capacity = capacity
        self.traffic_channels = traffic_channels
        self.ms_list = {}
        self.channels_in_use = 0
    
    def handle_connection_request(self, phone):
        """
        Pass the connection request to BSC
        """
        if len(self.ms_list) >= self.capacity:
            return False
        
        if self.bsc.handle_connection_request(self, phone):
            self.ms_list[phone.tmsi] = phone
            return True
        return False
        
    def make_call(self, calling_number, receiving_number):
        if self.channels_in_use == self.traffic_channels:
            return -1
        result = self.bsc.make_call(calling_number, receiving_number)
        if result == 0: # setup successful, assign a channel
            self.channels_in_use += 1
        return result
        
    def call_connect(self, tmsi, call_data):
        phone = self.ms_list.get(tmsi)
        phone.call_connect(call_data)
    
    def call_decline(self, tmsi):
        self.channels_in_use -= 1
        phone = self.ms_list.get(tmsi)
        phone.call_decline()
    
    def call_alert(self, tmsi, from_number):
        self.channels_in_use += 1
        phone = self.ms_list.get(tmsi)
        return phone.call_alert(from_number)
    
    def call_confirm(self, first_number, second_number, confirm): 
        if not confirm:
            self.channels_in_use -= 1
        return self.bsc.call_confirm(first_number, second_number, confirm)
        
    def request_end_call(self, first_number, second_number, in_call):
        return self.bsc.request_end_call(first_number, second_number, in_call)
    
    def end_call(self, tmsi):
        self.channels_in_use -= 1
        phone = self.ms_list.get(tmsi)
        phone.end_call()
    
    def send_sms(self, phone, number, message):
        self.bsc.send_sms(phone, number, message)
        
    def auth_challenge(self, phone, RAND):
        return phone.authenticate(RAND)
