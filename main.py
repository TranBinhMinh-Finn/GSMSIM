from components.bsc import BSC
from components.bts import BTS
from components.msc import MSC
from components.phone import Phone
from components.hlr_auc import HLR, HLR_data
from components.network import Network


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
        
phone_list.append(network.create_new_ms())
for bsc in network.msc.bsc_list:
    for bts in bsc.bts_list:
        if phone_list[-1].connect_to_bts(bts):
            break
    
phone_list[0].make_call(phone_list[1].number)
phone_list[1].request_end_call()
phone_list[0].make_call(phone_list[2].number)
phone_list[1].make_call(phone_list[2].number)