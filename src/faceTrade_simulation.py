import numpy as np

def faceTrade_simulation(charCfg_main,charCfg_target):

    # Simulation parameters.
    nSimulSamples   = charCfg_main.nSimulSamples

    # Counter the number of victory.
    numberVictory = 0

    for iter in range(nSimulSamples):

        charCfg_main.reset()
        charCfg_target.reset()

        # Action Time Battle based simulation.
        # Initial ATB is random with low arbitrary nitial value (way lower than 2/RPS),
        # to avoid having the same
        ATB_MC = np.random.random()/1000  # MC = Main Character.
        ATB_TC = np.random.random()/1000  # TC = Target Character.

        fightFinished = False

        while(not fightFinished):

            if ATB_TC < ATB_MC:

                if charCfg_target.isEmptyMag():
                    ATB_TC += charCfg_target.reload_time
                    charCfg_target.reload()
                else:
                    ATB_TC += 1/charCfg_target.RPS
                    charCfg_main.damage(charCfg_target.shoot())

                    if charCfg_main.isDead():
                        fightFinished = True


            else:

                if charCfg_main.isEmptyMag():
                    ATB_MC += charCfg_main.reload_time
                    charCfg_main.reload()
                else:
                    ATB_MC += 1/charCfg_main.RPS
                    charCfg_target.damage(charCfg_main.shoot())

                if charCfg_target.isDead():
                    fightFinished  = True
                    numberVictory += 1


    return numberVictory/nSimulSamples