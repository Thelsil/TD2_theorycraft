from src.faceTrade_simulation import faceTrade_simulation
from src.cfg.characterConfig import characterConfig

def optimalCoreDistribution(charCfg_main, shootingRange, bonusIWD=0, incrArmor=0, nSimulSamples=10**5):

    charCfg_target = characterConfig()
    charCfg_target.copy(charCfg_main)

    victoryRecord = {}

    for nrc_main in range(0, 6):

        victoryRecord[nrc_main] = []

        # Configure the main character with the new number of core.
        charCfg_main.nCores = [nrc_main, 6-nrc_main, 0]
        charCfg_main.configure_offense(bonusIWD)  # 10% bonus WD from Fenris piece.
        charCfg_main.configure_defense(incrArmor)

        for nrc_target in range(nrc_main+1, 7):

            print('Simulating with', str(nrc_main), 'red cores against',str(nrc_target),'red cores.')

            # Configure the target character with the new number of core.
            charCfg_target.nCores = [nrc_target, 6 - nrc_target, 0]
            charCfg_target.configure_offense(bonusIWD)  # 10% bonus WD from Fenris piece.
            charCfg_target.configure_defense(incrArmor)

            # Run the face trade simulation.
            simulResults = faceTrade_simulation(charCfg_main, charCfg_target, shootingRange, nSimulSamples)

            print('Probability of winning:',str(100*simulResults.probVictory),'%')
            victoryRecord[nrc_main].append(simulResults.probVictory)

    return victoryRecord