from src.cfg.characterConfig import characterConfig


def get_dummyBuild(nCores=6, useShield=True, hasUnbreakable=True, incrArmor=0, incrHealth=0):
    dummy_build = characterConfig()
    dummy_build.CHC = 0
    dummy_build.wpn_DMG = 0
    dummy_build.IWD = 0
    dummy_build.RPS = 1000
    dummy_build.MAG_size = 1
    dummy_build.reload_time = 1000
    dummy_build.CHD = 0
    dummy_build.HSD = 0
    dummy_build.DTA = 0
    dummy_build.OoCD = 0
    dummy_build.DTH = 0
    dummy_build.ProbHSD = 0
    dummy_build.ProbHIT = 0
    dummy_build.init_ATB = 10000
    dummy_build.nCores = [0,nCores,0]
    dummy_build.useShield = useShield
    dummy_build.configure_defense(incrArmor, incrHealth)

    if hasUnbreakable:
        dummy_build.chestTalent = 'Unbreakable'

    return dummy_build
