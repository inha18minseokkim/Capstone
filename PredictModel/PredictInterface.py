from abc import *
class PredictorInterface:
    @abstractmethod
    def __init__(self,isload=False):
        pass
    @abstractmethod
    def saveCurModel(self):
        pass
    @abstractmethod
    def loadCurModel(self):
        pass
    @abstractmethod
    def predict(self,code : list):
        pass
    @abstractmethod
    def loadDataSet(self, code : list):
        pass
    @abstractmethod
    def manipulateDataSet(self,prices):
        pass
    @abstractmethod
    def train(self,trainset,testset):
        pass