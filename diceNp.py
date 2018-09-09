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
        return type(self)(*zip(*m.items()))
    def __add__(self, d):
        return self.combine(sum, self, d)
    @classmethod
    def combine(cls, fn, *dice):
        return reduce(lambda acc, d: cls.combineAcross(fn, acc, d), dice)

    @classmethod
    def combineAcross(cls, fn, *dice):
        coaleseConst = lambda x: x if isinstance(x, cls) else cls.c(x)
        getItems = lambda x: coaleseConst(x).dict.items()
        diceVals = map(getItems, dice)
        cross = itertools.product(*diceVals)
        transposed = transpose(cross)
        pairIter = applyPermOp(fn, transposed)
        m = reduce(reduceToMap, pairIter, dict())
        return cls(*zip(*m.items()))

        
    def pmf(self):
        x,y = zip(*self.dict.items())
        return list(x), list(y)
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

class DictDieDivide(DictDie):
    @classmethod
    def combine(cls, fn, *dice):
        n = 2
        while len(dice) > 1:
            i = iter(dice)
            pairs = zip(*[i]*n)
            dice = list(map(lambda p: cls.combineAcross(fn, *p), pairs))
            dice += list(pairs)
        return dice[0]

    @classmethod
    def combineAcross(cls, fn, *dice):
        getItems = lambda x: dict.items((
            x if isinstance(x, cls)
            else cls.c(x)
        ).dict)
        diceVals = map(getItems, dice)
        cross = itertools.product(*diceVals)
        transposed = map(
            lambda perm: (
                fn(tuple(map(lambda pair: pair[0], perm))),
                prod(tuple(map(lambda pair: pair[1], perm)))
            ),
            cross
        )
        m = reduce(reduceToMap, transposed, dict())
        return cls(*zip(*m.items()))

class DictDieCache(DictDieDivide):
    @classmethod
    @functools.lru_cache()
    def combineAcross(cls, fn, *dice):
        return super(DictDieCache,DictDieCache).combineAcross(fn, *dice)

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
    def pmf(self):
        return self.val, self.prob
    def pool(self, n):
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
            # scale
            # add to acc
            # cont
        else:
            return reduceToMap(acc, pair)

class ArrayDicePool(DicePool):
    def best(self):
        return self.aggregate(np.maximum)
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
            dice = list(map(lambda p: cls.combineAcross(fn, *p), pairs))
            dice += list(pairs)
        return dice[0]

class ArrayDieDivideCache(ArrayDieDivide):
    @classmethod
    @functools.lru_cache()
    def combineAcross(cls, fn, *dice):
        return super(ArrayDieDivideCache,ArrayDieDivideCache).combineAcross(fn, *dice)
