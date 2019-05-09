import diceNp
from collections import defaultdict
from functools import reduce
import functools
import itertools
import numpy as np

class DefaultDict(diceNp.ArrayDieDivideCache):
    def map(self, fn):
        newVals = np.vectorize(fn)(self.val)
        m = reduce(self.reduceDieOrPairToMap, zip(newVals, self.prob), defaultdict(float))
        return type(self)(*zip(*m.items()))

    @classmethod
    @functools.lru_cache()
    def _combineTwo(cls, fn, a,b):
        aVal = a.val.reshape((-1, 1))
        bVal = b.val.reshape((1, -1))
        valMatrix = fn(aVal, bVal)

        aProb = a.prob.reshape((-1, 1))
        bProb = b.prob.reshape((1, -1))
        probsMatrix = np.multiply(aProb, bProb)
        m = reduce(reduceToMapDefaultDict, zip(valMatrix.flat, probsMatrix.flat), defaultdict(float))
        return cls(*zip(*m.items()))

    @classmethod
    def reduceDieOrPairToMap(cls, acc, pair):
        v, p = pair
        if isinstance(v, cls):
            return reduce(cls.reduceDieOrPairToMap, zip(v.val, (v.prob*p)), acc)
        else:
            return reduceToMapDefaultDict(acc, pair)

def reduceToMapDefaultDict(acc, pair):
    v, p = pair
    acc[v] += p
    return acc
