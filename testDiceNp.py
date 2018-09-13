import unittest
import diceNp
import numpy.testing as npt
import numpy as np
from samples import getToHit, getDamage

class TestDicePackage(unittest.TestCase):
    def setUp(self):
       self.dice = diceNp.ArrayDie
       self.assertArrEqual = npt.assert_array_equal
       self.assertArrFloatEqual = npt.assert_array_almost_equal

class TestDiceMethods(TestDicePackage):
    def test_n(self):
        a = self.dice.d(2)
        x,y = a.pmf()
        self.assertArrEqual(x, [1,2])
        self.assertArrEqual(y, [.5, .5])
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
        
    def test_mapToString(self):
        a = self.dice.d(3).map(lambda r: {
            1: "a",
            2: "b",
            3: "c"
            }[r])
        x,y = a.pmf()
        self.assertArrEqual(x, ["a", "b", "c"])
        self.assertArrEqual(y, [1./3, 1./3, 1./3])

    def test_mapStringValues(self):
        a = self.dice.d(3).map(lambda r: {
            1: "a",
            2: "a",
            3: "c"
            }[r]).map(lambda r: {
                "a": self.dice.d(2),
                "c": self.dice.d(2)+2
            }[r])
        x,y = a.pmf()
        self.assertArrEqual(x, [1,2,3,4])
        self.assertArrFloatEqual(y, [1./3, 1./3, 1./6, 1./6])

        """
    def test_combineSingleArray(self):
        self.dice.combine(
            np.sum,
            self.dice.d(20),
            self.dice.d(20),
            self.dice.d(20),
            self.dice.d(20),
        )
        """
    def test_combineTwoArray(self):
        x,y = self.dice.combine(
            np.add,
            self.dice.d(2),
            self.dice.d(2),
            self.dice.d(2),
            self.dice.d(2),
        ).pmf()
        self.assertArrEqual(x, [4,5,6,7,8])
        # self.assertArrFloatEqual(y, [1./3, 1./3, 1./6, 1./6])
        self.assertArrFloatEqual(y, np.array([1, 4, 6, 4, 1])/16.)
        #  1 3 3 1
        #L 0 1 3 3 1
        #U 1 3 3 1 0
        #  1 4 6 4 1
        
    def test_combineElements(self):
        x,y = self.dice.combineElements(
            lambda x,y: x.__add__(y),
            self.dice.d(2),
            self.dice.d(2),
            self.dice.d(2),
            self.dice.d(2),
        ).pmf()
        self.assertArrEqual(x, [4,5,6,7,8])
        # self.assertArrFloatEqual(y, [1./3, 1./3, 1./6, 1./6])
        self.assertArrFloatEqual(y, np.array([1, 4, 6, 4, 1])/16.)

    def test_combinePairList(self):
        x,y = self.dice.combinePerms(
            sum,
            self.dice.d(2),
            self.dice.d(2),
            self.dice.d(2),
            self.dice.d(2),
        ).pmf()
        self.assertArrEqual(x, [4,5,6,7,8])
        # self.assertArrFloatEqual(y, [1./3, 1./3, 1./6, 1./6])
        self.assertArrFloatEqual(y, np.array([1, 4, 6, 4, 1])/16.)

    """
    def test_guantlet(self):
        for i in range(3):
            a = self.dice.d(20).pool(2).best().map(getToHit(15, 7)).map(getDamage(self.dice.d(10), 6))
            x,y = a.pmf()
            print(list(x), list(y))
    """

    def test_map_immutable(self):
        a = self.dice.d(2)
        a.map(lambda v: self.dice.d(3))
        a.map(lambda v: 3)
        x,y = a.pmf()
        self.assertArrEqual(x, [1, 2])
        self.assertArrEqual(y, [.5, .5])

    def test_combBool(self):
        a = self.dice.d(2)
        b = self.dice.d(2)
        c = self.dice.combine(np.greater, a, b)
        x,y = c.pmf()
        self.assertArrEqual(x, [False, True])
        self.assertArrEqual(y, [.75, .25])

class TestDicePoolMethods(TestDicePackage):
    def test_add_pool(self):
        p = self.dice.d(2).pool(2)
        c = p.sum()
        x,y = c.pmf()
        self.assertArrEqual(x, [2, 3, 4])
        self.assertArrFloatEqual(y, [.25, .5, .25])

    def test_add_pool2x3(self):
        p = self.dice.d(2).pool(3)
        c = p.sum()
        x,y = c.pmf()
        self.assertArrEqual(x, [3, 4, 5, 6])
        self.assertArrFloatEqual(y, np.array([1, 3, 3, 1])/8.)
        
    def test_add_pool3x3(self):
        p = self.dice.d(3).pool(3)
        c = p.best()
        x,y = c.pmf()
        self.assertArrEqual(x, [1, 2, 3])
        self.assertArrFloatEqual(y, np.array([1, 7, 19])/27.)

    def test_add_pool5(self):
        p = self.dice.d(20).pool(5)
        c = p.sum()
        x,y = c.pmf()
        self.assertArrEqual(x, np.array(range(5,101)))
        # self.assertArrFloatEqual(y, [1])

    def test_gauntlet(self):
        p = self.dice.d(5).pool(2).best()
        x,y = p.pmf()
        self.assertArrEqual(x, [1,2,3,4,5])
        self.assertArrFloatEqual(y, np.array([1,3,5,7,9])/25)

class TestDiceArrayDivide(TestDicePoolMethods, TestDiceMethods):
    def setUp(self):
       super().setUp()
       self.dice = diceNp.ArrayDieDivide

class TestDiceArrayDivideCache(TestDicePoolMethods, TestDiceMethods):
    def setUp(self):
       super().setUp()
       self.dice = diceNp.ArrayDieDivideCache
