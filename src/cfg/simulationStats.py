class simulationStats:

    probVictory = None  # The probability that your character win the facetrade scenario.
    avg_TTK     = None  # The average time to kill your opponent.
    avg_TTD     = None  # The average time to die to your opponent.
    avg_eDPS    = None  # Your average effective DPS, corresponds to the average of the damage deal / simulation time.

    def display(self):

        print('Probability of victory:',str(100*self.probVictory),'%')
        print('Average time-to-kill:', str(self.avg_TTK), 's')
        print('Average time-to-die:', str(self.avg_TTD), 's')
        print('Average Effective DPS:', str(self.avg_eDPS/10**6), 'M dmg/s')


