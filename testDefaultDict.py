import defaultDict
import unittest
from testDiceNp import TestDicePoolMethods, TestDiceMethods
import operator

class TestDefaultDict(TestDicePoolMethods, TestDiceMethods):
    def setUp(self):
       super().setUp()
       self.dice = defaultDict.DefaultDict
