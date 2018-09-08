#/usr/env python3
import copy
import math
from fractions import Fraction

"""

2d6 -> roll 2 d6, sum them

1@2d6 -> roll 2 d6, take the larger
2@2d6 -> roll 2 d6, take the larger


"""

# does limiting probabilities to the numerator reduce complexity?
# can that be done and be valid?

class Outcome(object):
    def __init__(self, p, v):
        if type(p) is not Fraction:
            p = Fraction(p)
        self.prob = p
        self.val = v
    def __str__(self):
        return "({} {:.02%})".format(self.val, float(self.prob))
    def __repr__(self):
        return "({} {:.02%})".format(self.val, float(self.prob))
    def __add__(self, o):
        return self.combine(lambda x,y: x+y, o)

    def combine(self, fn, o):
        return Outcome(self.prob * o.prob, fn(self.val, o.val))

class Die(object):
    def __init__(self, outcomes=[]):
        if type(outcomes) != list:
            raise TypeError("wrong type passed to Die constructor")
        self.outcomes = self._cleanupOutcomes(outcomes)

    def map(self, fn):
        # res = []
        # for o in self.outcomes:
        outcomes = []
        for o in self.outcomes:
            v = fn(o.val)
            if type(v) == Die:
                scaled = map(lambda o2: Outcome(o2.prob * o.prob, o2.val), v.outcomes)
                outcomes.extend(scaled)
            else:
                outcomes.append(Outcome(o.prob, v))
        return Die(outcomes)
    
    def __add__(self, die):
        if type(die) != Die:
            return self + c(die)
        return self.combine(lambda x,y: x+y, die)

    def combine(self, fn, die):
        outcomes = [ x.combine(fn, y) for x in self.outcomes for y in die.outcomes]
        return Die(outcomes)

    def __str__(self):
        return "n={}, o={}".format(len(self), str(self.outcomes))
    def __repr__(self):
        return "<d, n={}>".format(len(self), repr(self.outcomes))

    def __len__(self):
        return len(self.outcomes)

    def avg(self):
        return sum([o.val * o.prob for o in self.outcomes])

    def pmf(self):
        m = { o.val: o.prob for o in self.outcomes }
        r = range(self.outcomes[0].val, self.outcomes[-1].val + 1)
        x, y = [], []
        for i in r:
            x.append(i)
            if i in m:
                y.append(float(m[i]))
            else:
                y.append(math.nan)
        return x,y

    def cmf(self, reverse=False):
        m = { o.val: o.prob for o in self.outcomes }
        r = range(self.outcomes[0].val, self.outcomes[-1].val + 1)
        if reverse:
            r = reversed(r)
        x, y = [], []
        total = 0
        for i in r:
            x.append(i)
            if i in m:
                total += float(m[i])
            y.append(total)
        if reverse:
            x.reverse()
            y.reverse()
        return x,y
        


    @staticmethod
    def d(stop, start=1):
        n = stop - start + 1
        prob = Fraction(1, n)
        outcomes = [Outcome(prob, v) for v in range(start, stop + 1)]
        return Die(outcomes)

    def pool(self, n):
        return DicePool([ copy.deepcopy(self) for n in range(n) ])
        
    @staticmethod
    def _cleanupOutcomes(outcomes):
        m = {}
        total = 0
        for o in outcomes:
            if o.val not in m:
                m[o.val] = Outcome(o.prob, o.val)
            else:
                m[o.val].prob += o.prob
            total += o.prob
        out = [o for o in m.values()]
        assert total == 1.0, "total:{} not 1: {}".format(total,out)
        return out

class DicePool(object):
    def __init__(self, pool=[]):
        self.pool = pool

    def sum(self):
        return self.aggregate(lambda a,b: a + b)

    def best(self):
        return self.aggregate(lambda x,y: max(x,y))

    def worst(self):
        return self.aggregate(lambda x,y: min(x,y))

    def aggregate(self, fn):
        i = iter(self.pool)
        try:
            acc = next(i)
        except StopIteration:
            return ValueError
        for d in i:
            acc = acc.combine(fn, d)
        return acc


d=Die.d
c=lambda n: d(n, n)
