import requests
import pandas as pd
class FinanceCrawl:
    def __init__(self):
        self.columns = "M111000,M113000,M122700,M221100,M312000,M314000,M382100".split(",")
    def convertToStr(self,code : list):
        res = ""
        for i in code:
            res += 'A' + i + ","
        return res[:-1]
    def getFinanceFrame(self,code : list):
        headers = {
            "key": "B8DE27145B59CF9845FE",
            "format": "json",
            "success": "true",
            "errcd": "",
            "errmsg": "",
            "code": self.convertToStr(code),
            "item": "M111000,M113000,M122700,M221100,M312000,M314000,M382100",
            "consolgb": "M",
            "annualgb": "QQ",
            "accdategb": "C",
            "fraccyear": "201203",
            "toaccyear": "202209"
        }
        url = "https://www.fnspace.com/Api/FinanceApi"
        res = requests.get(url, headers)
        resdict = res.json()
        resarr = []
        for ele in resdict['dataset']:
            for d in ele['DATA']:
                d['CODE'] = ele['CODE'][1:]
                resarr.append(d)
        df = pd.DataFrame(resarr)
        df = df.set_index([pd.to_datetime(df['DATE'].apply(lambda x : x + '01')),df['CODE']])
        df.drop(['DATE', 'YYMM', 'FS_YEAR', 'FS_MONTH', 'FS_QTR', 'MAIN_TERM'], axis=1, inplace=True)
        return df
    def getFinanceInfo(self,code : str):
        headers = {
            "key": "B8DE27145B59CF9845FE",
            "format": "json",
            "success": "true",
            "errcd": "",
            "errmsg": "",
            "code": "A" + code,
            "item": "M111000,M113000,M122700,M221100,M312000,M314000,M382100",
            "consolgb": "M",
            "annualgb": "QQ",
            "accdategb": "C",
            "fraccyear": "201203",
            "toaccyear": "202209"
        }
        url = "https://www.fnspace.com/Api/FinanceApi"
        res = requests.get(url, headers)
        resdict = res.json()
        resarr = []
        for ele in resdict['dataset']:
            for d in ele['DATA']:
                resarr.append(d)
        df = pd.DataFrame(resarr)
        df = df.set_index(pd.to_datetime(df['DATE'].apply(lambda x : x + '01')))
        df.drop(['DATE', 'YYMM', 'FS_YEAR', 'FS_MONTH', 'FS_QTR', 'MAIN_TERM'], axis=1, inplace=True)
        return df
if __name__ == "__main__":
    fc = FinanceCrawl()
    #print(fc.getFinanceFrame(['055550','003550','009200','000990','031440','009150','024110']))
    print(fc.getFinanceInfo('005930'))