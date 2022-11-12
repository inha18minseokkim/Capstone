class Starter:
    def __init__(self,stklist: str,strategy: int):
        self.stklist = stklist.split(",")
        self.strategy = strategy
    def rtnValue(self):
        return [self.stklist,self.strategy]