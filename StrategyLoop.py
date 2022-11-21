from enum import Enum

import Start
from Decide.Strategies import DefaultOptimizer,BlackLitterman
class Strategy(Enum):
    UserDefined = 0
    DefaultOptimizer = 1
    BlackLitterman = 2

class StrategyExecutor():
    def __init__(self):
        pass
    def bindStrategy(self,starter: Start.Starter):
        s = starter.rtnValue()
        code = s[0]
        strategy = s[1]
        period = s[2]
        if strategy == Strategy.UserDefined.value: # 0번 사용자 지정 모델
            pass
        if strategy == Strategy.DefaultOptimizer.value: # 1번 기본 최적화 알고리즘
            return DefaultOptimizer.DefaultOptimize(code,period)
        if strategy == Strategy.BlackLitterman.value: # 2번 블랙 리터만 모델
            return BlackLitterman.BlackLittermanStrategy(code,period)