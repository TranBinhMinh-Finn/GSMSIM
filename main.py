from components.bsc import BSC
from components.bts import BTS
from components.msc import MSC
from components.phone import Phone
from components.hlr_auc import HLR, HLR_data
from components.network import Network
"""
msc1 = MSC("network1")
bscList = []
btsList = []
phoneList = []

for i in (0,3):
    bsc = BSC(msc1, "bsc" + str(i))
    bscList.append(bsc)
    msc1.add_bsc(bsc)
    
for bsc in bscList:
    for i in (0,3):
        bts = BTS("bts" + str(i), bsc)
        btsList.append(bts)
        bsc.add_bts(bts)

for bts in btsList:
    phone = Phone(len(phoneList), "phone" + str(len(phoneList)))
    phoneList.append(phone)
    phone.connect_to_bts(bts=bts)
    
phoneList[0].call(1)
phoneList[2].call(1)
"""
network = Network("452", "01", "84", "91")
