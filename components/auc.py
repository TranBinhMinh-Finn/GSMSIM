import random
from algorithm.com128 import auth
def generate_triples(Ki):
    RAND = random(0, 65535)
    Kc, SRES = auth(Ki, RAND)
    return RAND, Kc, SRES