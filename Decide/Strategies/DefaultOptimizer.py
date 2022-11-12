import DataCollect
import Decide.Decider
from scipy.optimize import minimize
import numpy as np
class DefaultOptimize(Decide.Decider.DecisionMaker):
    def __init__(self,code,period):
        dc = DataCollect.DataCollector()
        self.code = code
        self.size = len(code)
        self.period = period
        self.rtn = dc.getRtn(dc.getPriceList(code),self.period)
        self.rtncorr = dc.getRtnCorr(self.rtn)
    def objfunc(self, w, rtncorr):
        return np.sqrt(w.T @ rtncorr @ w)
    def optimize(self):
        weights = np.array([1.0 / self.size] * self.size)
        bound = [(0, 1) for i in range(self.size)]
        params = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        res = minimize(self.objfunc, weights, self.rtncorr, method='SLSQP', bounds=bound, constraints=params)
        return res.x
    def process(self):
        ratio = self.optimize()
        res = {}
        for i in range(len(self.code)):
            res[self.code[i]] = ratio[i]
        return res
if __name__ == "__main__":
    do = DefaultOptimize(['005930','091170','003550','009200','261240','097950'],60)
    print(do.process())