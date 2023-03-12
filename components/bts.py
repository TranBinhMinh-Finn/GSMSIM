DEFAULT_CAPACITY = 100
DEFAULT_CHANNELS = 14

class BTS:
    def __init__(self, bsc, name = "bts", capacity = DEFAULT_CAPACITY, traffic_channels = DEFAULT_CHANNELS):
        self.name = name
        self.bsc = bsc
        self.capacity = capacity
        self.traffic_channels = traffic_channels
        self.ms_list = []
        self.channels_in_use = 0
    
    def handle_connection_request(self, phone):
        """
        Pass the connection request to BSC
        """
        if len(self.ms_list) >= self.capacity:
            return False
        
        if self.bsc.handle_connection_request(phone):
            self.ms_list.append(phone)
            return True
        return False
        
    def make_call(self, calling_number, receiving_number):
        if self.channels_in_use == self.traffic_channels:
            return -1
        return self.bsc.make_call(calling_number, receiving_number)
        
    def call_connect(self, phone, call_data):
        phone.call_connect(call_data)
        
    def call_confirm(self, phone, from_number): 
        return phone.call_confirm(from_number)
        
    def request_end_call(self, phone_number):
        return self.bsc.request_end_call(phone_number)
    
    def end_call(self, phone, call_data):
        self.channels_in_use -= 1
        phone.end_call(call_data)
    
    def send_sms(self, phone, number, message):
        self.bsc.send_sms(phone, number, message)
