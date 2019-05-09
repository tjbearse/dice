import experiment
import unittest
from testDiceNp import TestDicePoolMethods, TestDiceMethods
import operator

class TestExperiment(TestDicePoolMethods, TestDiceMethods):
    def setUp(self):
       super().setUp()
       self.dice = experiment.Experiment
