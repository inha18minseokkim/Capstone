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
        dc = DataCollector()
        fc = FinanceCrawl()
        prices = dc.getPriceList(code)
        tmprice = prices.iloc[-60:]
        tdaily = (tmprice - tmprice.shift(10)) / tmprice.shift(10)
        tweekly = (tmprice - tmprice.shift(20)) / tmprice.shift(20)
        tmonthly = (tmprice - tmprice.shift(40)) / tmprice.shift(40)
        tmpsample = pd.concat([tdaily.iloc[-1], tweekly.iloc[-1], tmonthly.iloc[-1]], axis=1)
        curmonth = tdaily.index[0].month
        if curmonth >= 1 and curmonth <= 3: targetdate = pd.Timestamp(year=tdaily.index[0].year, month=3, day=1)
        if curmonth >= 4 and curmonth <= 6: targetdate = pd.Timestamp(year=tdaily.index[0].year, month=6, day=1)
        if curmonth >= 7 and curmonth <= 9: targetdate = pd.Timestamp(year=tdaily.index[0].year, month=9, day=1)
        if curmonth >= 10 and curmonth <= 12: targetdate = pd.Timestamp(year=tdaily.index[0].year, month=12, day=1)
        print(curmonth)
        financedf = pd.DataFrame([],columns=fc.columns)
        for c in tmpsample.index:
            tmpdata = fc.getFinanceInfo(c).loc[targetdate]
            financedf.loc[c] = tmpdata
        tmpsample = pd.concat([tmpsample,financedf],axis=1)
        tmpsample.columns = ["daily", "weekly", "monthly"] + fc.columns
        print(tmpsample)

        res = self.model.predict(tmpsample)
        print(res)
        return self.getRes(code, res)

    def manipulateDataSet(self, prices):
        daily_shift = (prices - prices.shift(10)) / prices.shift(10)
        weekly_shift = (prices - prices.shift(20)) / prices.shift(20)
        monthly_shift = (prices - prices.shift(40)) / prices.shift(40)  # ??? ??? ????????? ????????? ?????????
        label_monthly_shift = monthly_shift.copy()
        x_set = pd.concat([daily_shift, weekly_shift, monthly_shift], axis=1).loc['2012-01-01':]
        y_set = label_monthly_shift.shift(-1).loc['2012-01-01':]
        daily_shift = daily_shift.loc["2012-01-01":] # fnguide ???????????? 10?????? ?????? ???????????? ??????????????? ????????? 2012????????? ??????
        weekly_shift = weekly_shift.loc["2012-01-01":]
        monthly_shift = monthly_shift.loc["2012-01-01":]
        li = []
        for i in prices.columns:  # ??? ???????????? ?????? ????????? ?????? ????????? ??? ????????? column??? 100x3 -> 100x1??????????????? 3 -> 1??? ??????
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
                except: #2022??? 12??? ?????? ?????????(??????) ?????? ????????? ????????? ????????? ?????? -> ?????? ?????????
                    pass
            tmp.columns = ['daily', 'weekly', 'monthly', 'label']
            tmp = pd.concat([tmp, restmp], axis=1)
            tmp.dropna()
            li.append(tmp)
        df = pd.concat(li).reset_index().drop(columns=['index'])
        df.dropna(inplace=True)
        print(df)
        trainset = lgb.Dataset(df.iloc[:-30].loc[:, df.columns.drop('label')].to_numpy(),
                               df.iloc[:-30].loc[:, ['label']].to_numpy())
        testset = lgb.Dataset(df.iloc[-30:].loc[:, df.columns.drop('label')].to_numpy(),
                              df.iloc[-30:].loc[:, ['label']].to_numpy())
        return [trainset, testset]

if __name__ == "__main__":
    fb = FinanceBooster()
    print(fb.predict(['055550','003550','009200','005930','024110']))