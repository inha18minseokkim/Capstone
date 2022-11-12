from abc import *

class DecisionMaker:
    #클래스의 기능 : 종목 코드를 받아서 종목들의
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def process(self):
        pass