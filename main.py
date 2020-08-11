from src.characterConfig import characterConfig
from src.faceTrade_simulation import faceTrade_simulation

nBlueCore_main   = 4
nBlueCore_target = 5

charCfg_main = characterConfig()
charCfg_main.CHC            = 0.6
charCfg_main.CHD            = 1.73
charCfg_main.HSD            = 0.9
charCfg_main.ProbHSD        = 0.25
charCfg_main.ProbHIT        = 0.75
charCfg_main.hasUnbreakable = True
charCfg_main.RPS            = 15
charCfg_main.MAG_size       = 50
charCfg_main.reload_time    = 2.2
charCfg_main.configure_defense(nBlueCore_main)

charCfg_target = characterConfig()
charCfg_target.copy(charCfg_main)
charCfg_main.configure_defense(nBlueCore_target)

# AR base damage * ( 1 + (10% SHD level + 25% WTD (fenris + AR) + 7% spec + 30% In Sync = 72%) + 15%*nRedCore)
# x 8% DTA x 18% OoCD x 10% concussion = 155.6% (note: no firewall dmg buff because this scenario is above 10m range)
# FAMAS base damage = 18560, RPS = 15
# FAL base damage   = 23890, RPS = 65/6, add +10% CHD (firewall mode)
charCfg_main.base_DMG   = 18560 * (1 + 0.62 + 0.15 * (6-nBlueCore_main))*1.4018
charCfg_target.base_DMG = 18560 * (1 + 0.72 + 0.15 * (6-nBlueCore_target))*1.4018

probVictory = faceTrade_simulation(charCfg_main, charCfg_target)
print(probVictory)

