import unittest
from dice import *

class TestOutcomeMethods(unittest.TestCase):
    def test_add(self):
        a = Outcome(1,2)
        b = Outcome(3,4)
        c = a + b
        self.assertEqual(c.prob, 3)
        self.assertEqual(c.val, 6)

class TestDiceMethods(unittest.TestCase):

    def test_add(self):
        a = d(2)
        b = d(2)
        c = a + b
        self.assertEqual([o.prob for o in c.outcomes], [.25, .5, .25])
        self.assertEqual([o.val for o in c.outcomes], [2, 3, 4])

    def test_map(self):
        a = d(2)
        c = a.map(lambda v: v+2)
        self.assertEqual([o.prob for o in c.outcomes], [.5, .5])
        self.assertEqual([o.val for o in c.outcomes], [3, 4])

    def test_map_die(self):
        a = d(2)
        c = a.map(lambda v: d(2))
        self.assertEqual([o.prob for o in c.outcomes], [.5, .5])
        self.assertEqual([o.val for o in c.outcomes], [1, 2])


class TestDicePoolMethods(unittest.TestCase):

    def test_add(self):
        p = d(2).pool(2)
        c = p.sum()
        self.assertEqual([o.prob for o in c.outcomes], [.25, .5, .25])
        self.assertEqual([o.val for o in c.outcomes], [2, 3, 4])
