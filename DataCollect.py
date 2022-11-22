import FinanceDataReader as fdr
import asyncio
import numpy as np
import pandas as pd

class DataCollector:
    def __init__(self):
        self.cap = fdr.StockListing('KRX-MARCAP')
        self.cap = self.cap.loc[:, ['Code', 'Marcap']]
        self.cap.set_index('Code', inplace=True)

    async def getPrice(self, code: str):
        res = fdr.DataReader(code)['Close']
        return res
    def getCodeList(self):
        return fdr.StockListing("KRX").loc[:,'Code'].tolist()

    async def getMarketCap(self, code: str):
        return self.cap.loc[code]['Marcap']

    def getPriceList(self, code: list):
        res = pd.concat([asyncio.run(self.getPrice(c)) for c in code],axis=1)
        res.columns = code
        return res
    def getRtn(self, df: pd.DataFrame, gap: int):
        rtn = ((df.shift(gap) - df) / df).dropna()
        return rtn
    def getRtnCorr(self, df : pd.DataFrame):
        return df.corr()
    def getMarketCapList(self, code: list):
        res = pd.DataFrame([asyncio.run(self.getMarketCap(c)) for c in code]).T
        res.columns = code
        return res

if __name__ == "__main__":
    dc = DataCollector()
    #print(dc.getRtn(dc.getPriceList(['055550','003550','009200','000990','031440']),30))
    #print(dc.getRtnCorr(dc.getRtn(dc.getPriceList(['055550', '003550', '009200', '000990', '031440']), 30)))
    #print(dc.getMarketCapList(['055550', '003550', '009200', '000990', '031440']))
    #print(asyncio.run(dc.getMarketCap('055550')))
    #print(asyncio.run(dc.getMarketCap('003550')))
    #print(dc.getCodeList())
    print(dc.getPriceList(dc.getCodeList()))