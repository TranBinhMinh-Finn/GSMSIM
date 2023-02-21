from components.hlr_auc import HLR
from components.vlr import VLR


class MSC:
    def __init__(self, name):
        self.name = name
        self.bsc_list = []
        self.hlr = HLR()
        self.vlr = VLR(self.hlr)
        self.eir = {}

    def add_bsc(self, bsc):
        self.bsc_list.append(bsc)
    
    def authenticate(self, phone):
        RAND, Kc, SRES = self.hlr.create_triplet(phone.imsi)
        if RAND == -1:
            # check hlr of other networks
            return False
        if SRES == phone.cal_SRES(RAND): # phone authenticate sucessfully
            # assign tmsi
            phone.tmsi = self.vlr.generate_tmsi()
            #TODO: update MS in VLR
            return True
        return False
    
    