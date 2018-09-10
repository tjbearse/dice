import numpy as np
import itertools
from fractions import Fraction
from functools import reduce
import functools
import operator
import copy


def prod(iterable):
    return reduce(operator.mul, iterable, 1)

class Die(object):
    # starting distribution
    def __init__(self, val, prob):
        pass
    def map(self, fn):
        pass
    def __add__(self, d):
        pass
    def pool(self, n):
        return DicePool([self for n in range(n)])
    def pmf(self):
        pass
    def adv(self):
        return self.pool(2).best()
    @classmethod
    def d(cls, stop, start=1):
        # n = stop - start + 1
        r = range(start, stop + 1)
        prob = float(1) / len(r)
        return cls(list(r), [prob for v in r])
    @classmethod
    def c(cls, n):
        return cls.d(n, n)

class DicePool(object):
    def __init__(self, dice):
        assert(len(dice) > 0)
        self.dice = dice
    def best(self):
        return self.aggregate(max)
    def sum(self):
        return self.aggregate(sum)
    def aggregate(self, fn):
        return self.dice[0].combine(fn, *self.dice)

def reduceToMap(acc, pair):
    v, p = pair
    if v in acc:
        acc[v] += p
    else:
        acc[v] = p
    return acc

class ArrayDie(Die):
    def __init__(self, val, prob):
        self.prob = np.array(prob)
        self.val = np.array(val)
    def map(self, fn):
        #FIXME vectorize doesn't like types to change between value and dice
        newVals = np.vectorize(fn)(self.val)
        m = reduce(self.reduceDieOrPairToMap, zip(newVals, self.prob), dict())
        return type(self)(*zip(*m.items()))
    def __add__(self, d):
        return self.combine(np.add, self, d)
    def avg(self):
        return sum(self.prob * self.val)
    def pmf(self):
        return self.val, self.prob
    def cmf(self, reverse=False):
        reverse = not reverse
        val = self.val
        prob = self.prob
        if reverse:
            prob = reversed(prob)
        prob = list(itertools.accumulate(prob))
        if reverse:
            prob =reversed(prob)
        return list(val), list(prob)
    def pool(self, n):
        assert(n > 0)
        return ArrayDicePool([self for n in range(n)])
    @classmethod
    def combine(cls, fn, *dice):
        coaleseConst = lambda x: x if isinstance(x, cls) else cls.c(x)
        ensuredDice = list(map(coaleseConst, dice))
        return reduce(lambda acc, d: cls.combineAcross(fn, acc, d), ensuredDice)

    # this is only performant across two dice, might fix it to that
    @classmethod
    def combineAcross(cls, fn, *dice):
        n = len(dice)
        vals = [cls.rotateShape(d.val, i, n) for i, d in enumerate(dice)]
        probs = [cls.rotateShape(d.prob, i, n) for i, d in enumerate(dice)]
        valMatrix = reduce(fn, vals)
        probsMatrix = reduce(np.multiply, probs)
        m = reduce(reduceToMap, zip(valMatrix.flat, probsMatrix.flat), dict())
        return cls(*zip(*m.items()))

    @staticmethod
    def rotateShape(arr, i, ndim):
        shapeBase = np.ones(ndim, int)
        shapeBase[i] = len(arr)
        return arr.reshape(shapeBase)

    @classmethod
    def reduceDieOrPairToMap(cls, acc, pair):
        v, p = pair
        if isinstance(v, cls):
            return reduce(reduceToMap, zip(v.val, (v.prob*p)), acc)
        else:
            return reduceToMap(acc, pair)

class ArrayDicePool(DicePool):
    def best(self):
        return self.aggregate(np.maximum)
    def worst(self):
        return self.aggregate(np.minimum)
    def sum(self):
        return self.aggregate(np.add)

class ArrayDieDivide(ArrayDie):
    @classmethod
    def combine(cls, fn, *dice):
        coaleseConst = lambda x: x if isinstance(x, cls) else cls.c(x)
        dice = list(map(coaleseConst, dice))
        n = 2
        while len(dice) > 1:
            i = iter(dice)
            pairs = zip(*[i]*n)
            if len(dice)%2 == 1:
                extra = [dice[-1]]
            else:
                extra = []
            dice = list(map(lambda p: cls.combineAcross(fn, *p), pairs))
            dice += extra
        return dice[0]

class ArrayDieDivideCache(ArrayDieDivide):
    @classmethod
    @functools.lru_cache()
    def combineAcross(cls, fn, *dice):
        return super(ArrayDieDivideCache,ArrayDieDivideCache).combineAcross(fn, *dice)
