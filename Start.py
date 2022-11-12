class Starter:
    def __init__(self,stklist: str,strategy: int,period : int):
        self.stklist = stklist.split(",")
        self.strategy = strategy
        self.period = period
    def rtnValue(self):
        return [self.stklist,self.strategy,self.period]