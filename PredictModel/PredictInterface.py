from abc import *
class PredictorInterface:

    def __init__(self,isload=False):
        try:
            if isload:
                print("Create New Model")
                raise Exception
            print("Load Existing Model...")
            self.model = self.loadCurModel()
            print("Load Existing model Completed")
        except:
            print("Create New Model")
            tmpcode = ['055550', '003550', '009200', '000990', '031440', '005930', '105560', '042700']
            self.prices = self.loadDataSet(tmpcode)
            self.trainset, self.testset = self.manipulateDataSet(self.prices)
            self.model = self.train(self.trainset, self.testset)
            self.saveCurModel()
            print("New Model Created Completely")
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