from DataCollect import DataCollector
import pandas as pd
import lightgbm as lgb
import numpy as np

from PredictModel.PredictInterface import PredictorInterface

MODELNAME = "LightGBM.boostregressor"
class BoostRegressor(PredictorInterface):
    def saveCurModel(self):
        self.model.save_model(MODELNAME)
    def loadCurModel(self):
        return lgb.Booster(model_file=MODELNAME)

    def getRes(self,code : list, prediction : np.ndarray):
        res = {}
        for i in range(len(code)):
            res[code[i]] = prediction[i]
        return res

    def predict(self,code: list):
        dc = DataCollector()
        prices = dc.getPriceList(code)
        tmprice = prices.iloc[-60:]
        tdaily = (tmprice - tmprice.shift(10)) / tmprice.shift(10)
        tweekly = (tmprice - tmprice.shift(20)) / tmprice.shift(20)
        tmonthly = (tmprice - tmprice.shift(40)) / tmprice.shift(40)
        tmpsample = pd.concat([tdaily.iloc[-1], tweekly.iloc[-1], tmonthly.iloc[-1]], axis=1)
        tmpsample.columns = ["daily", "weekly", "monthly"]
        print(tmpsample)
        res = self.model.predict(tmpsample)
        print(res)
        return self.getRes(code,res)


    def loadDataSet(self, code):
        dc = DataCollector()
        return dc.getPriceList(code)
    def manipulateDataSet(self,prices):
        daily_shift = (prices - prices.shift(10)) / prices.shift(10)
        weekly_shift = (prices - prices.shift(20)) / prices.shift(20)
        monthly_shift = (prices - prices.shift(40)) /prices.shift(40)  # 일 주 월별로 수익률 구한다
        label_monthly_shift = monthly_shift.copy()
        x_set = pd.concat([daily_shift, weekly_shift, monthly_shift], axis=1).loc['2003-01-01':'2022-09-25']
        y_set = label_monthly_shift.shift(-1).loc['2003-01-01':]

        li = []
        for i in prices.columns:  # 각 종목별로 있던 데이터 셋을 일렬로 쭉 나열함 column이 100x3 -> 100x1이었던것을 3 -> 1로 바꿈
            tmp = pd.concat([daily_shift.loc[:, i], weekly_shift.loc[:, i], monthly_shift.loc[:, i], y_set.loc[:, i]],
                            axis=1).reset_index().drop(columns=['Date'])
            tmp.columns = ['daily', 'weekly', 'monthly', 'label']
            li.append(tmp)
        df = pd.concat(li).reset_index().drop(columns=['index'])
        df.dropna(inplace=True)

        trainset = lgb.Dataset(df.iloc[:-30].loc[:, ['daily', 'weekly', 'monthly']].to_numpy(),
                               df.iloc[:-30].loc[:, ['label']].to_numpy())
        testset = lgb.Dataset(df.iloc[-30:].loc[:, ['daily', 'weekly', 'monthly']].to_numpy(),
                              df.iloc[-30:].loc[:, ['label']].to_numpy())
        return [trainset,testset]
    def train(self,trainset,testset):
        params = {'learning_rate': 0.001, 'max_depth': 16, 'boosting': 'gbdt',
                  'objective': 'regression', 'metric': 'mse', 'is_training_metric': True,
                  'num_leaves': 100, 'feature_fraction': 0.9, 'bagging_fraction': 0.7, 'bagging_freq': 5, 'seed': 2020}
        model = lgb.train(params, trainset, 1000, testset, verbose_eval=100, early_stopping_rounds=100)
        return model
if __name__ == "__main__":
    booster: BoostRegressor = BoostRegressor()
    print(booster.predict(['055550','003550','009200','005930','024110']))