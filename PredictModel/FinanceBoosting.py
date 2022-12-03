from DataCollect import DataCollector
from FinanceCrawler import FinanceCrawl
from PredictModel.BoostingRegrssor import BoostRegressor
import lightgbm as lgb
import pandas as pd
MODELNAME = 'FinanceBooster'
class FinanceBooster(BoostRegressor):

    def saveCurModel(self):
        self.model.save_model(MODELNAME)
    def loadCurModel(self):
        return lgb.Booster(model_file=MODELNAME)

    def predict(self, code: list):
        pass

    def manipulateDataSet(self, prices):
        fc = FinanceCrawl()
        daily_shift = (prices - prices.shift(10)) / prices.shift(10)
        weekly_shift = (prices - prices.shift(20)) / prices.shift(20)
        monthly_shift = (prices - prices.shift(40)) / prices.shift(40)  # 일 주 월별로 수익률 구한다
        label_monthly_shift = monthly_shift.copy()
        x_set = pd.concat([daily_shift, weekly_shift, monthly_shift], axis=1).loc['2012-01-01':]
        y_set = label_monthly_shift.shift(-1).loc['2012-01-01':]
        daily_shift = daily_shift.loc["2012-01-01":] # fnguide 크롤러가 10년치 밖에 데이터를 지원안해줌 그래서 2012년에서 끊어
        weekly_shift = weekly_shift.loc["2012-01-01":]
        monthly_shift = monthly_shift.loc["2012-01-01":]
        li = []
        for i in prices.columns:  # 각 종목별로 있던 데이터 셋을 일렬로 쭉 나열함 column이 100x3 -> 100x1이었던것을 3 -> 1로 바꿈
            tmp = pd.concat([daily_shift.loc[:, i].reset_index(), weekly_shift.loc[:, i].reset_index(),
                             monthly_shift.loc[:, i].reset_index(), y_set.loc[:, i].reset_index()], axis=1,
                            join='inner')
            tmp.index = tmp.iloc[:, 0]
            fc = FinanceCrawl()
            tmpfinanceinfo = fc.getFinanceInfo(i)
            tmp.drop(columns=['Date'], inplace=True)
            #print(tmp)
            restmp = pd.DataFrame([], columns=fc.columns)
            for j in tmp.index:
                if j.month >= 1 and j.month <= 3: tmpj = pd.Timestamp(year=j.year, month=3, day=1)
                if j.month >= 4 and j.month <= 6: tmpj = pd.Timestamp(year=j.year, month=6, day=1)
                if j.month >= 7 and j.month <= 9: tmpj = pd.Timestamp(year=j.year, month=9, day=1)
                if j.month >= 10 and j.month <= 12: tmpj = pd.Timestamp(year=j.year, month=12, day=1)
                try:
                    restmp.loc[j, fc.columns] = tmpfinanceinfo.loc[tmpj]
                except: #2022년 12월 같은 경우는(현재) 아직 결산이 안되서 데이터 없음 -> 예외 발생함
                    pass
            tmp.columns = ['daily', 'weekly', 'monthly', 'label']
            tmp = pd.concat([tmp, restmp], axis=1)
            tmp.dropna()
            li.append(tmp)
        df = pd.concat(li).reset_index().drop(columns=['index'])
        df.dropna(inplace=True)
        print(df)
        trainset = lgb.Dataset(df.iloc[:-30].loc[:, ['daily', 'weekly', 'monthly']].to_numpy(),
                               df.iloc[:-30].loc[:, ['label']].to_numpy())
        testset = lgb.Dataset(df.iloc[-30:].loc[:, ['daily', 'weekly', 'monthly']].to_numpy(),
                              df.iloc[-30:].loc[:, ['label']].to_numpy())
        return [trainset, testset]

if __name__ == "__main__":
    fb = FinanceBooster()