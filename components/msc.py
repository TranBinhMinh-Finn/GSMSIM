from components.hlr_auc import HLR

class MSC:
    def __init__(self, name):
        self.name = name
        self.bsc_list = []
        self.hlr = HLR()
        self.eir = {}

    def add_bsc(self, bsc):
        self.bsc_list.append(bsc)
    
    def authenticate(self, phone):
        RAND, Kc, SRES = self.hlr.create_triplet(phone.imsi)
        if RAND == -1:
            # check hlr of other networks
            return False
        if SRES == phone.cal_SRES(RAND):
            # gen TMSI
            return True
        return False
    
    