from components.bsc import BSC
from components.bts import BTS
from components.msc import MSC
from components.phone import Phone
from components.hlr_auc import HLR, HLR_data
from components.network import Network
import time
from utils import networks, network_code_mappings;
#number_of_present_calls, number_of_busy_calls, number_of_setup_fail_calls, number_of_success_calls 
import utils

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
        print(f"In ms {phone_number}, choose: (0: return / 1: call / 2: end call / 3: connect network / 4: show information)")
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
            print(f"Input mcc and mnc number of network: ")
            print(f"Mobile country code (mcc):")
            mcc = input()
            print(f"Mobile network code (mnc):")
            mnc = input()
            current_network = network_list.get((mcc, mnc))
            bts = phone.search_for_bts(current_network)
            if bts == None:
                print(f"Can't connect to this network.")
            else:
                print(f"Connect successfully")
                phone.connect_to_bts()
            continue
        if action == "4":
            phone.show_info()
            continue
        print(f"Type again.")

def network_interface():
    while True:
        print(f"Choose action: (0: return / 1: create new network / 2: access network / 3: show network list)")
        action = input()
        
        if action == "0":
            return
        
        if action == "1":
            print(f"Input mcc, mnc, cc, ndc of network: ")
            print(f"Mobile country code (mcc):")
            mcc = input()
            print(f"Mobile network code (mnc):")
            mnc = input()
            print(f"Country code (cc):")
            cc = input()
            print(f"National destination code (ndc):")
            ndc = input()
            network = Network(mcc, mnc, cc, ndc)
            network_list[(network.mcc, network.mnc)] = network
            
        if action == "2":
            print(f"Input mcc and mnc number of network: ")
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
                    print(f"In this network, choose: (0: return / 1: create new ms / 2: add bts / 3: show all ms in network / 4: show information of a number / 5: show the number of bts and bsc)")
                    action = input()
                    if action == "0":
                        return
                    if action == "1":
                        phone = current_network.create_new_ms()
                        print(f"Ms number {phone.number} has been created")
                        continue
                    if action == "2":
                        print(f"Type the number of bts you want to add: ")
                        number_bts = input()
                        while number_bts > 0:
                            current_network.add_bts()
                            number_bts -= 1
                    if action == "3":
                        current_network.show_all_ms()
                    if action == "4":
                        print(f"Type phone number: ")
                        number = input()
                        current_network.show_ms_info(number)
                    if action == "5":
                        current_network.show_number_bts_bsc()

        if action == "3":
            for network in networks.values():
                print(f"MCC: {network.mcc}, MNC: {network.mnc}, CC: {network.cc}, NDC: {network.ndc}")

def statistic_interface():
    while True:
        print(f"Choose action: (0: return / 1: show the number of call in present / 2: show calls statistic)")
        action = input()
        if action == "0":
            return
        if action == "1":
            print(f"There are (is) {utils.number_of_present_calls} call(s) in present.")
            continue
        if action == "2":
            success_rate = utils.number_of_success_calls * 1.0 / (utils.number_of_success_calls + utils.number_of_busy_calls + utils.number_of_setup_fail_calls) * 100
            setup_failure_rate = utils.number_of_setup_fail_calls * 1.0 / (utils.number_of_success_calls + utils.number_of_busy_calls + utils.number_of_setup_fail_calls) * 100
            busy_rate = utils.number_of_busy_calls * 1.0 / (utils.number_of_success_calls + utils.number_of_busy_calls + utils.number_of_setup_fail_calls) * 100
            print(f"There are (is) {utils.number_of_success_calls} success call(s). The rate is {success_rate}%.")
            print(f"There are (is) {utils.number_of_setup_fail_calls} set up failure call(s). The rate is {setup_failure_rate}%.")
            print(f"There are (is) {utils.number_of_busy_calls} busy call(s). The rate is {busy_rate}%.")
            continue
        print(f"Type again.")
        
while True:
    print(f"Access to :(1: network / 2: ms / 3: statistic)")
    s = input()
    while s != "1" and s != "2" and s != "3":
        print(f"Type again: (1: network / 2: ms / 3: statistic)")
        s = input()
    if s == "2":
        ms_interface()
    if s == "1":
        network_interface()
    if s == "3":
        statistic_interface()
             