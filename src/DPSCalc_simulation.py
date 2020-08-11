import numpy as np

def DPSCalc_simulation(characterConfig,target_eHP):

    # Simulation parameters.
    maxSavedBullets = characterConfig.maxSavedBullets
    nSimulSamples   = characterConfig.nSimulSamples

    # DPS calc parameters.
    RPS           = characterConfig.RPS
    MAG_size      = characterConfig.MAG_size
    reload_time   = characterConfig.reload_time
    timePerBullet = 1/RPS


    ProbBulletKill = np.zeros(maxSavedBullets)
    realDPS        = np.zeros(nSimulSamples)

    for iter in range(nSimulSamples):

        totalDamages = 0
        totalTime    = 0
        bulletCount  = 0
        magCount     = MAG_size

        while(totalDamages < target_eHP):

            if(magCount == 0):
                magCount   = MAG_size
                totalTime += reload_time
            else:

                bulletCount  += 1
                magCount     -= 1
                totalTime    += timePerBullet
                totalDamages += characterConfig.shoot()

        realDPS[iter] = target_eHP/totalTime
        if(bulletCount < maxSavedBullets):
            ProbBulletKill[bulletCount-1] += 1
        else:
            Warning(["Bullet count (" + str(bulletCount) + ") higher than max saved bullet. Consider increasing the later parameter."])


    realDPS        = np.mean(realDPS)
    ProbBulletKill = ProbBulletKill/nSimulSamples

    return [realDPS,ProbBulletKill]