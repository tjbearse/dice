import diceNp as d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import itertools

dice = d.ArrayDieDivideCache



def getToHit(ac, toHitConst):
    def toHit(roll):
        if roll == 20:
            return "crit"
        elif roll == 1:
            return "miss"
        elif roll + toHitConst > ac:
            return "hit"
        else:
            return "miss"
    return toHit

def getDamage(dmgDice, dmgConst):
    crit = dmgDice.pool(2).sum() + dmgConst
    hit = dmgDice + dmgConst
    def damage(outcome):
        if outcome == "crit":
            return crit
        elif outcome == "hit":
            return hit
        else:
            return dice.c(0)
    return damage


def hammerVsAxe():
    hammer = lambda ac: (
        dice.d(20).pool(2).best().map(getToHit(ac, 7)).map(getDamage(dice.d(10), 6)) +
        dice.d(20).map(getToHit(ac, 7)).map(getDamage(dice.d(10), 6)),
        "Hammer AC: {}".format(ac)
    )
    axe = lambda ac: (
        dice.d(20).pool(2).best().map(getToHit(ac, 7)).map(getDamage(dice.d(6), 6)) +
        dice.d(20).map(getToHit(ac, 7)).map(getDamage(dice.d(6), 6)) +
        dice.d(20).map(getToHit(ac, 7)).map(getDamage(dice.d(6), 2)),
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
    hammer = lambda ac, n: (
        dice.d(20).map(getToHit(ac, 7)).map(getDamage(dice.d(10), 6)).pool(2*n)
    )
    grapple = lambda ac, n: (
        dice.d(20).pool(2).best().map(getToHit(ac, 7)).map(getDamage(dice.d(10), 6)).pool(2*(n-1))
    )
    n = 6
    dmgH = [ hammer(ac, n).sum().avg() for ac in range(12, 22) ]
    dmgG = [ grapple(ac, n).sum().avg() for ac in range(12, 22) ]
    acs = list(range(12,22))

    ax = plt.subplot()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    ax.step(acs, dmgH, where='mid', label="hammer")
    ax.step(acs, dmgG, where='mid', label="grapple")
    ax.margins(0.05)
    ax.axis('tight')
    ax.legend()

    plt.show()

if __name__ == "__main__":
    hammerVsAxe()
