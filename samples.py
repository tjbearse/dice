import diceNp as d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import itertools
import numpy as np

dice = d.ArrayDieDivide



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

    acSet = [12, 15, 18]
    for d, l in itertools.chain(map(hammer, acSet), map(axe, acSet)):
        x, y = d.cmf()
        ax.step(x, y, label=l, where='mid')

    ax.margins(0.05)
    ax.axis('tight')
    ax.legend()

def hammerAvg():
    hammer = lambda ac, n: (
        dice.d(20).map(getToHit(ac, 7)).map(getDamage(dice.d(10), 6)).pool(2*n)
    )
    grapple = lambda ac, n: (
        dice.d(20).pool(2).best().map(getToHit(ac, 7)).map(getDamage(dice.d(10), 6)).pool(2*(n-1))
    )
    rounds = range(2,7)
    acs = range(12,22)
    dmgH = np.array([
        [hammer(ac, n).sum().avg() for n in rounds]
        for ac in acs
    ])
    dmgG = np.array([
        [grapple(ac, n).sum().avg() for n in rounds]
        for ac in acs
    ])
    combined = np.array([dmgG, dmgH])
    vmin, vmax  = np.amin(combined), np.amax(combined)

    fig, ((ax, ax2, ax3)) = plt.subplots(3, 1, figsize=(8, 6))
    shared = dict(ylabel="rounds", xlabel="ac", vmin=vmin, vmax=vmax)
    matPlotTable("WarHammer", dmgH.T, acs, rounds, ax=ax, **shared)
    im = matPlotTable("Grapple", dmgG.T, acs, rounds, ax=ax2, **shared)
    matPlotTable("Diff", (dmgG-dmgH).T, acs, rounds, ax=ax3, **{k:shared[k] for k in ["ylabel","xlabel"]})
    fig.tight_layout()
    cbar_ax = fig.add_axes([0.8, 0.09, 0.05, 0.85]) # L B W H
    fig.colorbar(im, cax=cbar_ax)

def highPoolTest():
    fig, (badax, goodax) = plt.subplots(2,1)
    for ax, impl in ((badax, d.ArrayDieDivide), (goodax, d.DictDie)):
        # needs a change to damage
        base = impl.d(20).map(getToHit(12, 7)).map(getDamage(impl.d(10), 6, impl.c(0)))
        for n in range(1,5):
            x,y = base.pool(n).sum().pmf()
            ax.step(x, y, label=n, where='mid')
    plt.legend()
    return

def grapple2d():
    stratNames = ("Straight")
    rollToDamage = lambda roll, ac: roll.map(getToHit(ac, 7)).map(getDamage(dice.d(10), 4))
    grapple = lambda opMod: dice.combine(
        np.greater,
        dice.d(20) + dice.c(7),
        dice.d(20) + dice.c(opMod)
    )
    stratList = (
        lambda ac, _, r: rollToDamage(dice.d(20)).pool(2*r).sum().avg(),
    )
    opModVals = range(0,8)
    opAcVals = range(12,22,3)
    rounds = 3
    sets = np.array([
        [
            [
                strat(ac, opMod, rounds)
                for opMod in opModVals
            ]
            for ac in opAcVals
        ]
        for strat in stratList
    ])
    vmin, vmax  = np.amin(sets), np.amax(sets)

    fig, axes = plt.subplots(len(sets)+1, 1, figsize=(8, 6))
    shared = dict(xlabel="ModValues", ylabel="AC", fmt="{:.0F}")
    for title, s, a in zip(stratNames, sets, (axes)):
        im = matPlotTable(title, s, opModVals, opAcVals, ax=a, **shared)
    fig.suptitle("Strategy damages over {} rounds".format(rounds))
    fig.tight_layout()
    # cbar_ax = fig.add_axes([0.8, 0.09, 0.05, 0.85]) # L B W H
    # fig.colorbar(im, cax=cbar_ax)

def matPlotTable(title, data, x, y,
                 fmt="{:2.0f}", ax=None, xlabel="x", ylabel="y", vmin=None, vmax=None):
    if ax is None:
        _, ax = plt.subplots()
    im = ax.imshow(data, cmap="viridis", interpolation=None,
              vmin=vmin, vmax=vmax
    )
    ax.set_title(title, loc="right")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x)
    ax.set_yticklabels(y)

    kw = dict(ha="center", va="center", color="w")
    threshold = im.norm(data.max())/2.
    textcolors = ["w", "k"]
    # Loop over data dimensions and create text annotations.
    for i in range(len(x)):
        for j in range(len(y)):
            kw.update(color=textcolors[int(im.norm(data[j, i]) > threshold)])
            text = ax.text(i, j, fmt.format(data[j, i]), **kw)

    return im

if __name__ == "__main__":
    hammerVsAxe()
    plt.show()
    hammerAvg()
    plt.show()
    grapple2d()
    plt.show()
