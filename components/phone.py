from algorithm.com128 import auth
from datetime import datetime
import utils

class Phone:
    def __init__(self, number, imsi, ki):
        self.number = number
        self.bts = None
        self.ki = ki
        self.kc = None
        self.lai = None
        self.imsi = imsi
        self.tmsi = None
        self.in_call = False
        self.from_number = None
        self.to_number = None
        self.wait_confirm = False
        self.decline = False
        self.call_data = None
        self.end_time = None
        self.wait_call = False

    def search_for_bts(self, network):
        bts = network.get_available_bts()
        return bts
    
    def connect_to_bts(self, bts):
        if bts.handle_connection_request(self):
            print(f'(MS {self.number}: Connected successfully.)')
            self.bts = bts
            return True
        print(f'(MS {self.number}: Failed to connect.)')
        return False

    def connect_to_network(self, network):
        self.connect_to_bts(self.search_for_bts(network))
    
    def authenticate(self, RAND):
        """
        Calculate SRES for challenge
        """
        Kc, SRES = auth(self.ki, RAND)
        return SRES

    def make_call(self, receiving_number):
        if not self.bts:
            if not self.connect_to_bts(self.search_for_bts()):
                print(f"(MS {self.number}: Failed to connect to network.)")
                return
        result = self.bts.make_call(self.number, receiving_number)
        if result == 1:
            print(f"(MS {self.number}: Receiver is busy.)")
            utils.number_of_busy_calls += 1
        if result == 2: 
            print(f"(MS {self.number}: Receiver doesn't exist)")
            utils.number_of_busy_calls += 1
        if result == -1:
            print(f"(MS {self.number}: Line busy)")
            utils.number_of_setup_fail_calls += 1
        if result == 0:
            utils.number_of_present_calls += 1
            utils.number_of_success_calls += 1
            self.wait_confirm = True
            self.to_number = receiving_number
    
    def call_connect(self, call_data):
        self.call_data = call_data
        number_call = call_data.second_number
        self.in_call = True
        self.to_number = number_call
        self.wait_confirm = False
        self.wait_call = False
    
    def call_decline(self):
        self.decline = True
        self.wait_confirm = False
    
    def call_alert(self, from_number):
        self.from_number = from_number
        return 0
    
    def check_state(self):
        if self.from_number != None: 
            print(f"(MS {self.number}: Receiving call from {self.from_number}...)")
            self.call_confirm()
        if self.in_call == True and self.wait_confirm == False:
            print(f"(MS {self.number}: In a call with {self.to_number}.)")
        if self.in_call == False and self.wait_confirm == True:
            print(f"(MS {self.number}: Calling {self.to_number}...)")    
        if self.decline == True:
            print(f"(MS {self.number}: Receiver {self.to_number} declined your call.)")
            self.decline = False
        if self.end_time != None:
            print(f"(MS {self.number}: Call end with {self.call_data.second_number} in {self.end_time - self.call_data.start_time}.)")
            self.end_time = None
    
    def call_confirm(self):
        print(f"Press Y to accept, N to decline: Y/N?")
        s = input()
        while s != 'Y' and s != 'N':
            print(f"{self.number}: Type again: (Y/N)")
            s = input()
        if s == 'Y':
            self.bts.call_confirm(self.number, self.from_number, True)
        else: 
            self.bts.call_confirm(self.number, self.from_number, False)
        self.from_number = None
    
    def request_end_call(self):
        result = self.bts.request_end_call(self.number, self.to_number, self.in_call)
        self.wait_confirm = False
        if result == True:
            print(f"(MS {self.number}: End successful.)")
            utils.number_of_present_calls -= 1
        else:
            print(f"(MS {self.number}: Fail to end call.)")
    
    def end_call(self):
        if not self.in_call:
            self.from_number = None
        else:
            self.in_call = False
            self.end_time = datetime.now()
    
    def show_info(self):
        print(f"Phone number: {self.number}")
        print(f"IMSI: {self.imsi}")
        print(f"Ki: {self.ki}")
    
    def text(self, receiving_number, message):
        self.bts.send_sms(self.number, receiving_number, message)
        
    def receive_sms(self, sending_number, message):
        print(f'{sending_number}:{message}')