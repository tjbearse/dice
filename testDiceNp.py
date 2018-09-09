import unittest
import diceNp
import numpy.testing as npt

class TestDicePackage(unittest.TestCase):
    def setUp(self):
       self.dice = diceNp.DictDie
       self.assertArrEqual = npt.assert_array_equal

class TestDiceMethods(TestDicePackage):
    def test_n(self):
        a = self.dice.d(2)
        x,y = a.pmf()
        self.assertArrEqual(x, [1,2])
        self.assertEqual(y, [.5, .5])
    def test_add(self):
        a = self.dice.d(2)
        b = self.dice.d(2)
        c = a + b
        x,y = c.pmf()
        self.assertArrEqual(x, [2, 3, 4])
        self.assertArrEqual(y, [.25, .5, .25])
    def test_add_const(self):
        a = self.dice.d(2)
        c = a + 2
        x,y = c.pmf()
        self.assertArrEqual(x, [3, 4])
        self.assertArrEqual(y, [.5, .5])

    def test_add_immutable(self):
        a = self.dice.d(2)
        c = a + 2
        x,y = a.pmf()
        self.assertArrEqual(x, [1, 2])
        self.assertArrEqual(y, [.5, .5])

    def test_map(self):
        a = self.dice.d(2)
        c = a.map(lambda v: v+2)
        x,y = c.pmf()
        self.assertArrEqual(x, [3, 4])
        self.assertArrEqual(y, [.5, .5])

    def test_map_die(self):
        a = self.dice.d(2)
        c = a.map(lambda v: self.dice.d(2))
        x,y = c.pmf()
        self.assertArrEqual(x, [1, 2])
        self.assertArrEqual(y, [.5, .5])

    def test_map_immutable(self):
        a = self.dice.d(2)
        a.map(lambda v: self.dice.d(3))
        a.map(lambda v: 3)
        x,y = a.pmf()
        self.assertArrEqual(x, [1, 2])
        self.assertArrEqual(y, [.5, .5])



class TestDicePoolMethods(TestDicePackage):
    def test_add(self):
        p = self.dice.d(2).pool(2)
        c = p.sum()
        x,y = c.pmf()
        self.assertArrEqual(x, [2, 3, 4])
        self.assertArrEqual(y, [.25, .5, .25])
