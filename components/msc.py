    
class MSC:
    def __init__(self, name):
        self.name = name
        self.bsc_list = []
        self.vlr = []
        self.hlr = []
        self.eir = []

    def add_bsc(self, bsc):
        self.bsc_list.append(bsc)

    def search_phone(self, number):
        for bsc in self.bsc_list:
            for bts in bsc.bts_list:
                for phone in bts.phones:
                    if phone.number == number:
                        return phone
        return None
    