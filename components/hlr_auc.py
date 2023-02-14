import random
from algorithm.com128 import auth

class HLR:
    def search_Ki(phone):
        #search
        return Ki
    
    def auth_check(phone):
        RAND = random(0, 65535)
        Kc, SRES = auth(Ki, RAND)
        Ki = HLR.search_Ki(phone)
        if(SRES == phone.cal_SRES(RAND)):
            return True
        return False