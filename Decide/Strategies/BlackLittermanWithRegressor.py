import numpy as np
from numpy.linalg import inv
import pandas as pd
import DataCollect
import DataRefiner
import Decide
from Decide.Strategies.BlackLitterman import BlackLittermanStrategy
from PredictModel.BoostingRegrssor import BoostRegressor


class BlackLittermanStrategyWithRegressor(BlackLittermanStrategy):
    def calc_QP(self):
        booster: BoostRegressor = BoostRegressor(False)
        resdict = booster.predict(self.code) #boostregressor 생성해서 코드에 맞게 예상수익률 산출
        resarr = []
        for i in self.code:
            resarr.append(resdict[i]) #코드 순서에 맞게 예쁘게 배열
        Q = np.array(resarr)
        P = np.eye(len(self.code))
        return [Q,P]
if __name__ == "__main__":
    blsr = BlackLittermanStrategyWithRegressor(  ['055550','003550','009200','000990','031440','009150','024110'], 60)
    print(blsr.w_mkt)
    print(blsr.process())