class JsonConvert:
    def __init__(self, target: dict):
        self.target = target
    def rtnTo(self):
        ratiolist = []
        for k,v in self.target.items():
            ratiolist.append({"stockId":str(k),"rate":str(v)})
        print(ratiolist)
        return {"ratioList":ratiolist}
