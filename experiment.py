import diceNp
from defaultDict import DefaultDict
from collections import defaultdict
from numbers import Number
from functools import reduce
import functools
import itertools
import operator
import numpy as np


class Experiment(DefaultDict):
    @classmethod
    @functools.lru_cache()
    def _combineTwo(cls, fn, a,b):
        aVal = a.val.reshape((-1, 1))
        bVal = b.val.reshape((1, -1))
        valMatrix = fn(aVal, bVal)

        aProb = a.prob.reshape((-1, 1))
        bProb = b.prob.reshape((1, -1))
        probsMatrix = np.multiply(aProb, bProb)
        # stacking to sort
        stacked = np.stack([valMatrix.flat, probsMatrix.flat])
        # sorting by one column is a bit odd...
        stacked = stacked[:,stacked[0,:].argsort()]

        # now for accumulating duplicates
        vals, index = np.unique(stacked[0], return_index=True)
        probs = np.empty_like(vals, dtype=probsMatrix.dtype)
        for i, (start, stop) in enumerate(pairwise(index)):
            probs[i] = np.add.reduce(stacked[1,start:stop])

        probs[-1] = np.add.reduce(stacked[1, index[-1]:])

        return cls(vals, probs)

def pairwise(i):
    a,b = itertools.tee(i)
    next(b, None)
    return zip(a,b)

def reduceToMapB(acc, pair):
    v, p = pair
    acc[v] += p
    return acc
