import dice
import diceNp
import timeit
import typing
from samples import getToHit, getDamage

diceImpl : typing.Any

def timeThis(s, d):
    global diceImpl
    diceImpl = d
    return "{:.4f}".format(timeit.timeit(s, number=100, globals=globals()))

def printResults(results, implNames):
    row_format ="{:>20}" + "{:>10}" * len(implNames)
    print(row_format.format("", *implNames))
    for row in results:
        print(row_format.format(*row))

poolSize = 20
tests = [
    ("d20 init x2", 'diceImpl.d(20), diceImpl.d(20)'),
    ("d20 add", 'diceImpl.d(20) + diceImpl.d(20)'),
    ("d20 add via pool", 'diceImpl.d(20).pool(2).sum()'),
    ("d20 best", 'diceImpl.d(20).pool(2).best()'),
    ("gauntlet", 'diceImpl.d(20).pool(2).best().map(getToHit(15, 7)).map(getDamage(diceImpl.d(10), 6))'),
]

impls = [
    # (diceNp.DictDie, "dict"),
    # (diceNp.DictDieDivide, "divide"),
    # (diceNp.DictDieCache, "cache"),
    (diceNp.ArrayDie, "array"),
    (diceNp.ArrayDieDivide, "arrdiv"),
    (diceNp.ArrayDieDivideCache, "arrdiv$"),
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
