from components.hlr_auc import HLR
from components.vlr import VLR, VLR_data


class MSC:
    def __init__(self, name):
        self.name = name
        self.bsc_list = []
        self.hlr = HLR()
        self.vlr = VLR()
        self.eir = {}

    def add_bsc(self, bsc):
        self.bsc_list.append(bsc)
    
    def authenticate(self, phone):
        RAND, Kc, SRES = self.hlr.create_triplet(phone.number)
        if RAND == -1:
            #TODO: check hlr of other networks
            return False
        if SRES == phone.cal_SRES(RAND): # phone authenticate sucessfully
            # assign tmsi
            phone.tmsi = self.vlr.generate_tmsi()
            self.vlr.add_ms(phone.number, VLR_data(phone.imsi, phone.tmsi, False))
            self.hlr.update_vlr(phone.number, self.vlr)
            return True
        return False
    
    