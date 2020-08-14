import numpy as np
from src.cfg.simulationStats import simulationStats


def faceTrade_simulation(charCfg_main, charCfg_target, shootingRange=15, nSimulSamples=10 ** 6, verbose=False):
    # Counter the number of victory.
    numberVictory = 0
    avgTTK = 0
    avgTTD = 0
    avg_eDPS = 0

    for iter in range(nSimulSamples):

        if 10 < nSimulSamples:
            if iter % round(nSimulSamples / 10) == 0:
                print('Simulation processing: ', str(round(100 * iter / nSimulSamples)), '%')

        charCfg_main.init(shootingRange)
        charCfg_target.init(shootingRange)
        totalDmg = 0

        # Action Time Battle based simulation.
        # Initial ATB is random with low arbitrary nitial value (way lower than 2/RPS),
        # to avoid having the same
        ATB_MC = charCfg_main.init_ATB + np.random.random() / 1000  # MC = Main Character.
        ATB_TC = charCfg_target.init_ATB + np.random.random() / 1000  # TC = Target Character.

        fightFinished = False

        if verbose:
            print('-----------------')
            print('Starting round ', str(iter))

        while not fightFinished:

            if verbose:
                print('')
                print('MC ATB = ', str(ATB_MC))
                print('TC ATB = ', str(ATB_TC))

                MC_eHP = charCfg_main.effectiveHitPoints()
                print('MC has ', str(MC_eHP[0]), ' armors, ',
                      str(MC_eHP[1]), ' health, ',
                      str(MC_eHP[2]), ' shield HP')

                TC_eHP = charCfg_target.effectiveHitPoints()
                print('TC has ', str(TC_eHP[0]), ' armors, ',
                      str(TC_eHP[1]), ' health, ',
                      str(TC_eHP[2]), ' shield HP')

            if ATB_TC < ATB_MC:

                if charCfg_target.isEmptyMag():
                    time = charCfg_target.reload_time
                    charCfg_target.reload()

                    if verbose:
                        print('TC is reloading!')
                else:
                    time = 1 / charCfg_target.RPS
                    hasArmor = charCfg_main.hasArmor()
                    hasShield = charCfg_main.shieldDeployed()

                    if verbose:
                        charCfg_main.damage(charCfg_target.shoot(hasArmor, hasShield), 'MC')
                    else:
                        charCfg_main.damage(charCfg_target.shoot(hasArmor, hasShield))

                    ATB_TC += time
                    charCfg_target.updateCooldown(time)

                    if charCfg_main.isDead():
                        avgTTD += ATB_TC
                        fightFinished = True

                        if verbose:
                            print('MC is killed! Defeat!')



            else:

                if charCfg_main.isEmptyMag():
                    time = charCfg_main.reload_time
                    charCfg_main.reload()

                    if verbose:
                        print('MC is reloading!')
                else:
                    time = 1 / charCfg_main.RPS
                    hasArmor = charCfg_target.hasArmor
                    asShield = charCfg_target.shieldDeployed()

                    dmgVect = charCfg_main.shoot(hasArmor, asShield)
                    totalDmg += dmgVect[0]
                    if verbose:
                        charCfg_target.damage(dmgVect, 'TC')
                    else:
                        charCfg_target.damage(dmgVect)

                ATB_MC += time
                charCfg_main.updateCooldown(time)

                if charCfg_target.isDead():
                    fightFinished = True
                    avgTTK += ATB_MC
                    numberVictory += 1

                    if verbose:
                        print('TC is killed! Victory!')

        avg_eDPS += totalDmg / ATB_MC

    simulResults = simulationStats()
    simulResults.probVictory = numberVictory / nSimulSamples

    if 0 < numberVictory:
        simulResults.avg_TTK = avgTTK / numberVictory
    else:
        simulResults.avg_TTK = None

    if 0 < (nSimulSamples - numberVictory):
        simulResults.avg_TTD = avgTTD / (nSimulSamples - numberVictory)
    else:
        simulResults.avg_TTD = None

    simulResults.avg_eDPS = avg_eDPS / nSimulSamples

    print('Simulation finished.')
    print('')

    return simulResults
