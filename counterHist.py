from diceNp import Die
from collections import Counter
from numbers import Number
from functools import reduce
import operator

class CounterHist(Die):
    # starting distribution
    def __init__(self, m=None):
        if m is not None:
            self.counter = Counter(m)
        else:
            self.counter = Counter()
        
    def map(self, fn):
        m = dict()
        dice = False
        for k, v in self.counter.items():
            newK = fn(k)
            if isinstance(newK, Die):
                dice = True
            m[k] = newK
        if dice:
            return self.__mapToDie(m)
        else:
            return self.__mapToThing(m)

    def __mapToThing(self, m):
        newC = CounterHist()
        for k in self.counter.keys():
            newKey = m[k]
            newC.counter[newKey] += self.counter[k]
        return newC

    def __mapToDie(self, m):
        newC = CounterHist()
        sums = { k: sum(v.counter.values()) for k, v in m.items() }
        factor = reduce(operator.mul, sums.values())

        for k1 in m.keys():
            v1 = self.counter[k1]
            hist = m[k1]
            s = sums[k1]
            adjCount = v1 * factor / s
            for k2,v2 in hist.counter.items():
                newC.counter[k2] += adjCount*v2
        return newC

    def __add__(self, d):
        if isinstance(d, Number):
            return CounterHist({ k+d: v for k,v in self.counter.items() })
            
        return self.map(lambda k: d+k)
        """
        newC = CounterHist()
        for k1, v1 in self.counter.items():
            for k2, v2 in d.counter.items():
                newC.counter[k1+k2] += v1+v2
        return newC
        """
                
    def pool(self, n):
        return DicePool([self for n in range(n)])

    def pmf(self):
        s = sum(self.counter.values())
        sort = sorted(self.counter.items(), key=operator.itemgetter(0))
        keys, values = zip(*sort)
        values = map(lambda x: x/s, values)
        return list(keys), list(values)

    @classmethod
    def d(cls, stop, start=1):
        # n = stop - start + 1
        r = range(start, stop + 1)
        prob = float(1) / len(r)
        return cls({v: 1 for v in r})

def mergeBest(a, b):
    bsum = sum(b.counter.values())
    bsort = list(sorted(b.counter.items(), reverse=True, key=operator.itemgetter(0)))
    return a.map(getBestDieFn(bsort, bsum))

# b should be reverse sorted
def getBestDieFn(bsort, bsum):
    def getBestDie(k):
        c = CounterHist()
        running = 0
        for kb, vb in bsort:
            if kb > k:
                c.counter[kb] += vb
                running += vb
            else:
                c.counter[k] = bsum - running
                return c
    return getBestDie

class DicePool(object):
    def __init__(self, dice):
        assert(len(dice) > 0)
        self.dice = dice

    def best(self):
        return reduce(mergeBest, self.dice)
    #TODO test whether divide and conquer reduce helps

    def sum(self):
        return reduce(operator.add, self.dice)
