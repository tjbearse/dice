#/usr/env python3
import copy

"""

2d6 -> roll 2 d6, sum them

1@2d6 -> roll 2 d6, take the larger
2@2d6 -> roll 2 d6, take the larger


"""

# does limiting probabilities to the numerator reduce complexity?
# can that be done and be valid?

class Outcome(object):
    def __init__(self, c, v):
        self.count = c
        self.val = v
    def __str__(self):
        return "({} x{})".format(self.val, self.count)
    def __repr__(self):
        return "({} x{})".format(self.val, self.count)
    def __add__(self, o):
        return self.combine(lambda x,y: x+y, o)

    def combine(self, fn, o):
        return Outcome(self.count + o.count -1, fn(self.val, o.val))

class Die(object):
    def __init__(self, outcomes=[]):
        if type(outcomes) != list:
            raise TypeError("wrong type passed to Die constructor")
        self.outcomes = self._cleanupOutcomes(outcomes)

    def map(self, fn):
        return Die(map(lambda o: Outcome(o.count, fn(o.val))))

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
        """
        # sum
        c = 0
        for o in self.outcomes:
            c += o.count
        """
        return len(self.outcomes)

    @staticmethod
    def d(stop, start=1):
        n = stop - start + 1
        outcomes = [Outcome(1, v) for v in range(start, stop + 1)]
        return Die(outcomes)

    def pool(self, n):
        return DicePool([ copy.deepcopy(self) for n in range(n) ])
        
    @staticmethod
    def _cleanupOutcomes(outcomes):
        m = {}
        for o in outcomes:
            if o.val not in m:
                m[o.val] = Outcome(o.count, o.val)
            else:
                m[o.val].count += o.count
        return [o for o in m.values()]

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
