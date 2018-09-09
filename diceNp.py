import numpy as np
import itertools
from fractions import Fraction
from functools import reduce
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
        pass
    def pmf(self):
        pass
    @classmethod
    def d(cls, stop, start=1):
        n = stop - start + 1
        prob = float(1) / n
        r = range(start, stop + 1)
        return cls(list(r), [prob for v in r])
    @classmethod
    def c(cls, n):
        return cls.d(n, n)

class DicePool(object):
    def __init__(self, dice):
        self.dice = dice
    def best(self):
        return self.aggregate(max)
    def sum(self):
        return self.aggregate(sum)
    def aggregate(self, fn):
        return self.dice[0].combine(fn, *self.dice)

class DictDie(Die):
    def __init__(self, val, prob):
        self.dict = { v: p for v,p in zip(val, prob) }
    def map(self, fn):
        update = map(lambda x: (fn(x[0]), x[1]), self.dict.items())
        m = reduce(reduceDieOrPairToMap, update, dict())
        return DictDie(*zip(*m.items()))
    def __add__(self, d):
        return self.combine(sum, self, d)
    @classmethod
    def combine(cls, fn, *dice):
        coaleseConst = lambda x: x if isinstance(x, DictDie) else cls.c(x)
        getItems = lambda x: coaleseConst(x).dict.items()
        diceVals = map(getItems, dice)
        cross = itertools.product(*diceVals)
        transposed = transpose(cross)
        pairIter = applyPermOp(fn, transposed)
        m = reduce(reduceToMap, pairIter, dict())
        return DictDie(*zip(*m.items()))
        
        
    def pmf(self):
        x,y = zip(*self.dict.items())
        return list(x), list(y)
    def pool(self, n):
        return DicePool([self for n in range(n)])


def transpose(permIter):
    # iter for (v,p),(v,p)...
    return map(
        lambda perm: (
            tuple(map(lambda pair: pair[0], perm)),
            tuple(map(lambda pair: pair[1], perm))
        ),
        permIter
    )
def applyPermOp(fn, permIter):
    return map(lambda pair: (fn(pair[0]), prod(pair[1])), permIter)

def reduceDieOrPairToMap(acc, pair):
    v, p = pair
    if isinstance(v, DictDie):
        return reduce(reduceToMap, map(lambda x: (x[0], x[1]*p), v.dict.items()), acc)
        # scale
        # add to acc
        # cont
    else:
        return reduceToMap(acc, pair)
        

def reduceToMap(acc, pair):
    v, p = pair
    if v in acc:
        acc[v] += p
    else:
        acc[v] = p
    return acc
