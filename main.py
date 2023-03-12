from components.bsc import BSC
from components.bts import BTS
from components.msc import MSC
from components.phone import Phone
from components.hlr_auc import HLR, HLR_data
from components.network import Network
import time
from utils import network_db, network_code_mappings

network = Network("452", "01", "84", "91")
network.add_bts()
phone_list = [] 
phone_list.append(network.create_new_ms())

for bsc in network.msc.bsc_list:
    for bts in bsc.bts_list:
        if phone_list[-1].connect_to_bts(bts):
            break

phone_list.append(network.create_new_ms())
for bsc in network.msc.bsc_list:
    for bts in bsc.bts_list:
        if phone_list[-1].connect_to_bts(bts):
            break

network = Network("452", "02", "84", "98")
network.add_bts()
        
phone_list.append(network.create_new_ms())
for bsc in network.msc.bsc_list:
    for bts in bsc.bts_list:
        if phone_list[-1].connect_to_bts(bts):
            break
        
phone_list.append(network.create_new_ms())
for bsc in network.msc.bsc_list:
    for bts in bsc.bts_list:
        if phone_list[-1].connect_to_bts(bts):
            break
"""    
phone_list[0].make_call("66330000000003")
time.sleep(5)
phone_list[1].request_end_call()
phone_list[0].make_call(phone_list[2].number)
phone_list[1].make_call(phone_list[2].number)
time.sleep(5)
phone_list[0].request_end_call()
phone_list[2].request_end_call()
"""

while True:
    print(f"Access to :(1: network / 2: msc / 3: bsc / 4: bts / 5: ms)")
    s = input()
    while s != "1" and s != "2" and s != "3" and s != "4" and s != "5":
        print(f"Type again: (1: network / 2: msc / 3: bsc / 4: bts / 5: ms)")
        s = input()
    if s == "5":
        phone_number = "-1"
        while phone_number != "0":
            print(f"Phone number: ")
            phone_number = input()
            if(phone_number == "0"):
                break
            cc = phone_number[0:2]
            ndc = phone_number[2:4]
            if len(phone_number) < 4:
                print(f"Wrong phone number. Type again.")
                continue
            network_code = network_code_mappings.get((cc, ndc))
            if network_code == None:
                print(f"Wrong phone number. Type again.")
                continue
            else:
                hlr = network_db.get(network_code)
                if hlr == None: # Can't find hlr 
                    print(f"Wrong phone number. Type again.")
                    continue
                if hlr.search_phone(phone_number) != None:
                    current_vlr = hlr.ms_db[phone_number].serving_vlr
                    phone = current_vlr.search_phone(phone_number).ms
                else: # Can't find phone in hlr
                    print(f"Wrong phone number. Type again.")
                    continue
            # check receive call
            phone.call_alert()
            if(phone.from_number != None): 
                phone.call_confirm()
            #print(f"In ms {phone_number}, choose: (0: return / 1: call / 2: end call / 3: connect network")
            while True:
                print(f"In ms {phone_number}, choose: (0: return / 1: call / 2: end call / 3: connect network)")
                action = input()
                if action == "0":
                    break
                if action == "1":
                    print(f"Type number you want to call: ")
                    receive_number = input()
                    phone.make_call(receive_number)
                    continue
                if action == "2":
                    phone.request_end_call()
                    continue
                if action == "3":
                    phone.connect_to_bts(phone.search_for_bts())
                    continue
                print(f"Type again.")
            
             