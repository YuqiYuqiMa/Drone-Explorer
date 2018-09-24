# ======================================================================
# FILE:        Distribution.py
#
# DESCRIPTION: Contains distribution: exponential, random
#
# ======================================================================

import random
import Arena


class Distribution:
    def __init__(self, v):
        self.var = v

    def random20(self):
        time = 0
        num = 0
        while num != 1:
            time += 1
            num = random.randint(1, 5)
        return time

    def exponential(self):
        return random.expovariate(self.var)
