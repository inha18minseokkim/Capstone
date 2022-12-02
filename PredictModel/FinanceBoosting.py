from PredictModel.PredictInterface import PredictorInterface
import lightgbm as lgb
MODELNAME = 'FinanceBooster'
class FinanceBooster(PredictorInterface):

    def saveCurModel(self):
        self.model.save_model(MODELNAME)
    def loadCurModel(self):
        return lgb.Booster(model_file=MODELNAME)

    def predict(self, code: list):
        pass

    def loadDataSet(self, code: list):
        pass

    def manipulateDataSet(self, prices):
        pass

    def train(self, trainset, testset):
        pass