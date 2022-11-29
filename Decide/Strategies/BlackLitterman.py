import numpy as np
from numpy.linalg import inv
import pandas as pd
import DataCollect
import DataRefiner
import Decide.Decider


class BlackLittermanStrategy(Decide.Decider.DecisionMaker):
    def __init__(self,code,period):
        self.code = code
        self.period = period
        self.size = len(code)
        dc = DataCollect.DataCollector()
        self.rtn = dc.getRtn(dc.getPriceList(code),self.period)
        self.rtncorr = dc.getRtnCorr(self.rtn)
        self.mktCap = dc.getMarketCapList(code)
        #print(self.mktCap)
        #print(np.sum(self.mktCap,axis=1))
        self.w_mkt = DataRefiner.getWMkt(self.mktCap)
    def calc_QP(self):
        Q = np.array([1, 1, 1])
        P = np.ones([3, len(self.code)])
        return [Q,P]
    def dataprepro(self):
        expected_rtn = self.rtn.mean().multiply(self.w_mkt).sum()
        portfolio_variance = self.w_mkt.dot(self.rtncorr).dot(self.w_mkt)
        lambd = expected_rtn / portfolio_variance
        Pi = lambd * self.rtncorr.dot(self.w_mkt)
        QP = self.calc_QP()
        Q = QP[0]
        P = QP[1]
        tau = 1
        Omega = tau * P.dot(self.rtncorr).dot(P.T) * np.eye(len(Q))
        ER = Pi * tau * self.rtncorr.dot(P.T).dot(inv(P.dot(tau * self.rtncorr).dot(P.T) + Omega).dot(Q - P.dot(Pi)))
        w_hat = inv(self.rtncorr).dot(ER)
        w_hat = pd.Series(w_hat / w_hat.sum(), index=self.code)
        print(w_hat,np.sum(w_hat))
        w_hat -= np.min(w_hat)
        w_hat /= np.sum(w_hat)
        print(w_hat,np.sum(w_hat))
        return w_hat
    def process(self):
        ratio = self.dataprepro()
        res = {}
        for i in range(len(self.code)):
            res[self.code[i]] = ratio.iloc[i]
        return res

if __name__ == "__main__":
    bls = BlackLittermanStrategy( ['055550','003550','009200','000990','031440','005930','105560','042700'], 60)
    print(bls.w_mkt)
    print(bls.process())
