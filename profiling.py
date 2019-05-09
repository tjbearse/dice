import cProfile
import experiment


diceImpl = experiment.Experiment
poolSize = 30

profiles = [
    # ("best2", 'diceImpl.d(20).pool({}).best()'.format(2)),
    # ("sum2", 'diceImpl.d(20).pool({}).sum()'.format(2)),
    ("best", 'diceImpl.d(20).pool({}).best()'.format(poolSize)),
    ("sum", 'diceImpl.d(20).pool({}).sum()'.format(poolSize)),
]

for (n,p) in profiles:
    print("""
======================================
==         {}
======================================
    """.format(n))
    cProfile.run(p)
