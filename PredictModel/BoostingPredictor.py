from DataCollect import DataCollector
import pandas as pd
import lightgbm as lgb
import numpy as np
MODELNAME = "LightGBM.booster"
class Booster:
    def categorize(self,earning, q1, q2, q3, q4):
        if earning < q1: return 1
        if earning < q2: return 2
        if earning < q3: return 3
        if earning < q4: return 4
        return 5
    def __init__(self,isload = False):
        try:
            if isload:
                print("Create New Model")
                raise Exception
            print("Load Existing Model...")
            self.model = self.loadCurModel()
            print("Load Existing model Completed")
        except:
            print("Create New Model")
            tmpcode = ['055550','003550','009200','000990','031440','005930','105560','042700']
            self.prices = self.loadDataSet(tmpcode)
            self.trainset,self.testset = self.manipulateDataSet(self.prices)
            self.model = self.train(self.trainset,self.testset)
            self.saveCurModel()
            print("New Model Created Completely")
    def saveCurModel(self):
        self.model.save_model(MODELNAME)
    def loadCurModel(self):
        return lgb.Booster(model_file=MODELNAME)

    def getRank(self,code : list, prediction : np.ndarray):
        res = {}
        for i in range(len(code)):
            cnt = 1
            for j in range(len(prediction)):
                if i == j: continue
                if prediction[i] < prediction[j]: cnt+= 1
            res[code[i]] = cnt
        return res

    def predict(self,code: list):
        dc = DataCollector()
        prices = dc.getPriceList(code)
        tmprice = prices.iloc[-60:]
        tdaily = (tmprice - tmprice.shift(1)) / tmprice.shift(1)
        tweekly = (tmprice - tmprice.shift(20)) / tmprice.shift(20)
        tmonthly = (tmprice - tmprice.shift(50)) / tmprice.shift(50)
        tmpsample = pd.concat([tdaily.iloc[-1], tweekly.iloc[-1], tmonthly.iloc[-1]], axis=1)
        tmpsample.columns = ["daily", "weekly", "monthly"]
        return self.getRank(code,self.model.predict(tmpsample))


    def loadDataSet(self, code):
        dc = DataCollector()
        return dc.getPriceList(code)
    def manipulateDataSet(self,prices):
        daily_shift = (prices - prices.shift(1)) / prices.shift(1)
        weekly_shift = (prices - prices.shift(20)) / prices.shift(20)
        monthly_shift = (prices - prices.shift(50)) /prices.shift(50)  # 일 주 월별로 수익률 구한다
        label_monthly_shift = monthly_shift.copy() #여기다가 01 분류값 넣을거임

        for i in monthly_shift.index:
            med = monthly_shift.loc[i].median()  # 중간값 구해서
            label_monthly_shift.loc[i] = monthly_shift.loc[i] > med  # 중간값보다 큰놈은 1 작은놈은 0 이런식으로 분류 데이터를 만든다

        label_monthly_shift = label_monthly_shift.astype(int)  # True False를 1 0으로 바꿈
        x_set = pd.concat([daily_shift, weekly_shift, monthly_shift], axis=1).loc['2003-01-01':'2022-07-25']
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
                  'objective': 'binary', 'metric': 'mse', 'is_training_metric': True,
                  'num_leaves': 100, 'feature_fraction': 0.9, 'bagging_fraction': 0.7, 'bagging_freq': 5, 'seed': 2020}
        model = lgb.train(params, trainset, 1000, testset, verbose_eval=100, early_stopping_rounds=100)
        return model
if __name__ == "__main__":
    booster: Booster = Booster(False)
    print(booster.predict(['055550','003550','009200','005930','024110']))