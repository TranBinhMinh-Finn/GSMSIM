from algorithm.com128 import auth
from datetime import datetime
import utils

class Phone:
    def __init__(self, number, imsi, ki):
        self.number = number
        self.bts = None
        self.network = None
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
        self.message = []

    def search_for_bts(self, network):
        bts = network.get_available_bts()
        return bts
    
    def connect_to_bts(self, bts):
        if bts is not None:
            if bts.handle_connection_request(self):
                print(f'(MS {self.number}): Connected successfully.')
                self.bts = bts
                return True
        print(f'(MS {self.number}): Failed to connect.')
        return False

    def disconnect_from_bts(self):
        if self.bts is None:
            return
        self.bts.disconnect_ms(self)
        self.bts = None
        
    def connect_to_network(self, network):
        if self.bts is not None:
            self.disconnect_from_bts()
        self.network = network
        self.connect_to_bts(self.search_for_bts(network))
    
    def authenticate(self, RAND):
        """
        Calculate SRES for challenge
        """
        Kc, SRES = auth(self.ki, RAND)
        return SRES

    def check_connection(func):
        def wrapper(*args, **kwargs):
            ms=args[0]
            if ms.bts is None:
                print(f"(MS {ms.number}): Not connected to any network.")
                return
            func(*args, **kwargs)
        
        return wrapper
    
    @check_connection 
    def make_call(self, receiving_number):
        # if self.bts is None:
        #     print(f"(MS {self.number}): Not connected to any network.")
        #     return
        
        result = self.bts.make_call(self.number, receiving_number)
        if result == 1:
            print(f"(MS {self.number}): Receiver is busy.")
            utils.number_of_busy_calls += 1
        if result == 2: 
            print(f"(MS {self.number}): Receiver doesn't exist.")
            utils.number_of_setup_fail_calls += 1
        if result == -1:
            print(f"(MS {self.number}): Line busy.")
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
            print(f"(MS {self.number}): Receiving call from {self.from_number}...")
            self.call_confirm()
        if self.in_call == True and self.wait_confirm == False:
            print(f"(MS {self.number}): In a call with {self.to_number}.")
        if self.in_call == False and self.wait_confirm == True:
            print(f"(MS {self.number}): Calling {self.to_number}...")    
        if self.decline == True:
            print(f"(MS {self.number}): Receiver {self.to_number} declined your call.")
            self.decline = False
        if self.end_time != None:
            print(f"(MS {self.number}): Call end with {self.call_data.second_number} in {self.end_time - self.call_data.start_time}.")
            self.end_time = None
        message_unread = 0
        for message in self.message:
            if message[3] == False:
                message_unread += 1
        if message_unread > 0:
            print(f"(MS {self.number}): There are (is) {message_unread} unread message.") 
                
    
    def call_confirm(self):
        print(f"(MS {self.number}): Press Y to accept, N to decline: Y/N?")
        s = input()
        while s != 'Y' and s != 'N':
            print(f"(MS {self.number}): Type again: (Y/N)")
            s = input()
        if s == 'Y':
            self.bts.call_confirm(self.number, self.from_number, True)
        else: 
            self.bts.call_confirm(self.number, self.from_number, False)
        self.from_number = None
    
    @check_connection
    def request_end_call(self):
        result = self.bts.request_end_call(self.number, self.to_number, self.in_call)
        self.wait_confirm = False
        if result == True:
            print(f"(MS {self.number}): End successful.")
            utils.number_of_present_calls -= 1
        else:
            print(f"(MS {self.number}): Fail to end call.")
    
    def end_call(self):
        if not self.in_call:
            self.from_number = None
        else:
            self.in_call = False
            self.end_time = datetime.now()
    
    def show_info(self):
        print(f"(MS {self.number}): ")
        print(f"Phone number: {self.number},")
        print(f"IMSI: {self.imsi},")
        print(f"Ki: {self.ki},")
        print(f"In network: mcc = {self.network.mcc}, mnc = {self.network.mnc}.")
    
    def show_message_info(self, id):
        self.message[id][3] = True
        print(f"(MS {self.number}): From {self.message[id][0]}, at {self.message[id][2]}")
        print(f"Message: {self.message[id][1]}")
    
    def show_all_message(self):
        id_last = len(self.message) - 1
        if id_last == -1:
            print(f"No received message.")
            return
        while True:
            id = id_last
            print(f"(MS {self.number}): ")
            while id >= id_last - 4:
                if id < 0: 
                    break
                if self.message[id][3] == False:
                    print(f"{id_last - id + 1}: Message from {self.message[id][0]}, at {self.message[id][2]} (unread).")
                else:
                    print(f"{id_last - id + 1}: Message from {self.message[id][0]}, at {self.message[id][2]}.")
                id -= 1
            print(f"Choose action: (0: return / 1: previous / 2: next / 3: read message)")
            action = input()
            if action == "0":
                return
            if action == "1":
                if id_last >= 5: 
                    id_last -= 5
            if action == "2":
                if id_last < len(self.message) - 1:
                    id_last += 5
            if action == "3":
                print(f"Choose message you want to read or type 0 to return:")
                while True:
                    id = int(input())
                    if id == 0:
                        break
                    if id <= 5 and id >= 1 and id_last - id + 1 >= 0:
                        self.show_message_info(id_last - id + 1)
                        break
                    print(f"(MS {self.number}): Type again.")
                print(f"(MS {self.number}): Type something to return.")
                input()
    
    @check_connection
    def text(self, receiving_number, message):
        send_time=datetime.now()
        result = self.bts.send_sms(self.number, receiving_number, send_time, message)
        if result == 0: 
            print(f"(MS {self.number}): Send message successfully.")
        else:
            print(f"(MS {self.number}): Fail to send message.")
        
    def receive_sms(self, sending_number, send_time, message):
        self.message.append([sending_number, message, send_time, False])
        #print(f'{sending_number}:{message}')