import numpy as np
from numpy.linalg import inv
import pandas as pd
import DataCollect
import DataRefiner
import Decide
from Decide.Strategies.BlackLitterman import BlackLittermanStrategy

class BlackLittermanStrategyWithRegressor(BlackLittermanStrategy):
    def calc_QP(self):
        Q = np.array([0.07669642, 0.09424969, 0.18199817, 0.12835284, -0.02027411, 0.13328767, 0.10802241])
        P = np.eye(len(self.code))
        return [Q,P]
if __name__ == "__main__":
    blsr = BlackLittermanStrategyWithRegressor(  ['055550','003550','009200','000990','031440','009150','024110'], 60)
    print(blsr.w_mkt)
    print(blsr.process())