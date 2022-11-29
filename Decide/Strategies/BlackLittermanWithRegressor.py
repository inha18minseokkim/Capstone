import numpy as np
from numpy.linalg import inv
import pandas as pd
import DataCollect
import DataRefiner
import Decide.Decider

class BlackLittermanStrategyWithRegressor(Decide.Strategies.BlackLitterman.BlackLittermanStrategy):
    def calc_QP(self):
        pass
    def dataprepro(self):
        pass

if __name__ == "__main__":
    blsr = BlackLittermanStrategyWithRegressor( ['055550','003550','009200','000990','031440','005930','105560','042700'], 60)
    print(blsr.w_mkt)
    print(blsr.process())