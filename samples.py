import dice
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import itertools



def getToHit(ac, toHitConst, dmgDice, dmgConst):
    def toHit(roll):
        if roll == 20:
            return dmgDice.pool(2).sum() + dice.c(dmgConst)
        elif roll == 1:
            return 0
        elif roll + toHitConst > ac:
            return dmgDice + dice.c(dmgConst)
        else:
            return 0
    return toHit


def hammerVsAxe():
    hammer = lambda ac: (
        dice.d(20).pool(2).best().map(getToHit(ac, 7, dice.d(10), 6)) +
        dice.d(20).map(getToHit(ac, 7, dice.d(10), 6)),
        "Hammer AC: {}".format(ac)
    )
    axe = lambda ac: (
        dice.d(20).pool(2).best().map(getToHit(ac, 7, dice.d(6), 6)) +
        dice.d(20).map(getToHit(ac, 7, dice.d(6), 6)) +
        dice.d(20).map(getToHit(ac, 7, dice.d(6), 2)),
        "Axe AC: {}".format(ac)
    )
    ax = plt.subplot()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    acSet = [ 15 ]
    for d, l in itertools.chain(map(hammer, acSet), map(axe, acSet)):
        x, y = d.cmf(True)
        ax.step(x, y, label=l, where='mid')

    ax.margins(0.05)
    ax.axis('tight')
    ax.legend()

    plt.show()

def hammerAvg():
    hammer = lambda ac: (
        dice.d(20).map(getToHit(ac, 7, dice.d(10), 6)) +
        dice.d(20).map(getToHit(ac, 7, dice.d(10), 6))
    )
    dmg = [ hammer(ac).avg() for ac in range(12, 22) ]
    acs = list(range(12,22))

    ax = plt.subplot()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    print(acs, dmg)
    ax.step(acs, dmg, where='mid')
    ax.margins(0.05)
    ax.axis('tight')

    plt.show()

def hammerAvg():
    hammer = lambda ac: (
        dice.d(20).map(getToHit(ac, 7, dice.d(10), 6)) +
        dice.d(20).map(getToHit(ac, 7, dice.d(10), 6))
    )
    dmg = [ hammer(ac).avg() for ac in range(12, 22) ]
    acs = list(range(12,22))

    ax = plt.subplot()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    print(acs, dmg)
    ax.step(acs, dmg, where='mid')
    ax.margins(0.05)
    ax.axis('tight')

    plt.show()

hammerAvg()
