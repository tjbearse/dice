import counterHist
from testDiceNp import TestDicePoolMethods, TestDiceMethods

class TestCountHist(TestDicePoolMethods, TestDiceMethods):
    def setUp(self):
       super().setUp()
       self.dice = counterHist.CounterHist
