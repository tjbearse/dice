import diceNp
import counterHist
import timeit
import typing
from experiment import Experiment
from defaultDict import DefaultDict
from samples import getToHit, getDamage

def timeThis(s, d):
    global diceImpl
    diceImpl = d
    return "{:.4f}".format(timeit.timeit(s, number=100, globals=globals()))

def printResults(results, implNames):
    row_format ="{:>20}" + "{:>10}" * len(implNames)
    print(row_format.format("", *implNames))
    for row in results:
        print(row_format.format(*row))

poolSize = 25
tests = [
    ("d20 init x2", 'diceImpl.d(20), diceImpl.d(20)'),
    ("d20 add", 'diceImpl.d(20) + diceImpl.d(20)'),
    ("c map", 'diceImpl.d(20).map(lambda x:2)'),
    ("dice map", 'diceImpl.d(20).map(lambda x: diceImpl.d(8))'),
    ("d20 add via pool", 'diceImpl.d(20).pool(2).sum()'),
    ("d20 add via pool x4", 'diceImpl.d(20).pool(4).sum()'),
    ("d20 best", 'diceImpl.d(20).pool(2).best()'),
    ("d20 x4 best", 'diceImpl.d(20).pool(5).best()'),
]

impls = [
    # (diceNp.ArrayDie, "array"),
    (Experiment, "exp"),
    (diceNp.ArrayDieDivide, "arrdiv"),
    (diceNp.ArrayDieDivideCache, "arrdiv$"),
    #(counterHist.CounterHist, "c"),
    (DefaultDict, "dd"),
    #, dice.Die]: 
    ]

"""
results = ([testName] + [timeThis(t,d) for d,iname in impls] for testName, t in tests)
printResults(results, list(map(lambda x: x[1], impls)))
"""



print("\nlarge pools")
largeTests = [
    ("best", 'diceImpl.d(20).pool({}).best()'.format(poolSize)),
    ("sum", 'diceImpl.d(20).pool({}).sum()'.format(poolSize)),
]
results = ([testName] + [timeThis(t,d) for d,iname in impls] for testName, t in largeTests)
printResults(results, list(map(lambda x: x[1], impls)))
