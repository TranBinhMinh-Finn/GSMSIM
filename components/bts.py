
class BTS:
    def __init__(self, name, bsc):
        self.name = name
        self.bsc = bsc
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)
        return True