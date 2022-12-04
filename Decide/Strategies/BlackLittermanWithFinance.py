import numpy as np

from Decide.Strategies.BlackLitterman import BlackLittermanStrategy
from PredictModel.FinanceBoosting import FinanceBooster


class BlackLittermanStrategyWithFnguide(BlackLittermanStrategy):
    def calc_QP(self):
        booster: FinanceBooster = FinanceBooster()
        resdict = booster.predict(self.code) #boostregressor 생성해서 코드에 맞게 예상수익률 산출
        resarr = []
        for i in self.code:
            resarr.append(resdict[i]) #코드 순서에 맞게 예쁘게 배열
        Q = np.array(resarr)
        P = np.eye(len(self.code))
        return [Q,P]

if __name__ == "__main__":
    blsr = BlackLittermanStrategyWithFnguide(  ['055550','003550','009200','000990','031440','009150','024110'], 60)
    print(blsr.w_mkt)
    print(blsr.process())