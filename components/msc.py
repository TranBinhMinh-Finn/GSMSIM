    
class MSC:
    def __init__(self, name, hlr):
        self.name = name
        self.bsc_list = []
        self.hlr = hlr
        self.eir = {}

    def add_bsc(self, bsc):
        self.bsc_list.append(bsc)
    
    def auth_check(self, phone):
        RAND, Kc, SRES = self.hlr.trans_triples(phone)
        if(SRES == phone.cal_SRES(RAND)):
            return True
        return False
    
    