import dice
import diceNp
import timeit
import typing
from samples import getToHit, getDamage

diceImpl : typing.Any

def timeThis(l, s):
    print(l, "\t", timeit.timeit(s, number=100, globals=globals()))

poolSize = 3

for d in [diceNp.DictDie, dice.Die]: 
    diceImpl = d
    print("start")
    timeThis("d20 init x2", 'diceImpl.d(20), diceImpl.d(20)')
    timeThis("d20 add", 'diceImpl.d(20) + diceImpl.d(20)')
    timeThis("d20 add via pool", 'diceImpl.d(20).pool(2).sum()')

    timeThis("d20 best", 'diceImpl.d(20).pool(2).best()')

    timeThis("gauntlet", 'diceImpl.d(20).pool(2).best().map(getToHit(15, 7)).map(getDamage(diceImpl.d(10), 6))')

    print("\n\nlarge pools")
    timeThis("best", 'diceImpl.d(20).pool({}).best()'.format(poolSize))
    timeThis("sum", 'diceImpl.d(20).pool({}).sum()'.format(poolSize))
    print("stop")
