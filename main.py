from components.bsc import BSC
from components.bts import BTS
from components.msc import MSC
from components.phone import Phone
from components.hlr_auc import HLR, HLR_data
from components.network import Network
import time
from utils import networks, network_code_mappings

network_list = {}
network = Network("452", "01", "84", "91")
network_list[(network.mcc, network.mnc)] = network
network.add_bts()
phone_list = [] 
phone_list.append(network.create_new_ms())
phone_list[-1].connect_to_network(network)

phone_list.append(network.create_new_ms())
phone_list[-1].connect_to_network(network)

network = Network("452", "02", "84", "98")
network_list[(network.mcc, network.mnc)] = network
network.add_bts()
        
phone_list.append(network.create_new_ms())
phone_list[-1].connect_to_network(network)
        
phone_list.append(network.create_new_ms())
phone_list[-1].connect_to_network(network)
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

def ms_interface():
    print(f"Input phone number of MS, or enter 0 to return: ")
    phone_number = ""
    while phone_number != "0":
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
            network = networks.get(network_code)
            if network is None: # Can't find hlr 
                print(f"Wrong phone number. Type again.")
                continue
            hlr = network.hlr
            if hlr.search_phone(phone_number) != None:
                current_vlr = hlr.ms_db[phone_number].serving_vlr
                phone = current_vlr.search_phone(phone_number).ms
                break
            else: # Can't find phone in hlr
                print(f"Wrong phone number. Type again.")
                continue
    # check receive call
    #print(f"In ms {phone_number}, choose: (0: return / 1: call / 2: end call / 3: connect network")
    while True:
        phone.check_state()
        print(f"In ms {phone_number}, choose: (0: return / 1: call / 2: end call / 3: connect network)")
        action = input()
        if action == "0":
            return
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

def network_interface():
    while True:
        print(f"Input mcc and mnc number of network, or enter 0 to return: ")
        print(f"Mobile country code (mcc):")
        mcc = input()
        print(f"Mobile network code (mnc):")
        mnc = input()
        current_network = network_list.get((mcc, mnc))
        if current_network == None: 
            print(f"This network doesn't exist, type again.")
            continue
        else:
            while True:
                print(f"In this network, choose: (0: return / 1: create new ms / )")
                action = input()
                if action == "0":
                    return
                if action == "1":
                    phone = current_network.create_new_ms()
                    print(f"Ms number {phone.number} has been created")
                    continue
            #return

    

while True:
    print(f"Access to :(1: network / 2: ms)")
    s = input()
    while s != "1" and s != "2":
        print(f"Type again: (1: network / 2: ms)")
        s = input()
    if s == "2":
        ms_interface()
    if s == "1":
        network_interface()
        
            
             