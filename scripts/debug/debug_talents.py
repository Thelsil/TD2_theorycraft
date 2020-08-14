from scripts.builds.get_TrashBuild import get_TrashBuild
from scripts.builds.get_dummyBuild import get_dummyBuild
from src.faceTrade_simulation import faceTrade_simulation

VERBOSE       = False
shootingRange = 10

trashBuild = get_TrashBuild()
dummyBuild = get_dummyBuild()

trashBuild.wpn_DMG = trashBuild.wpn_DMG/10
trashBuild.weaponTalent = None
trashBuild.backpackTalent = None
trashBuild.chestTalent = None

wpnTalentList      = ['In Sync','Optimist','Strained','Sadistic','Ignited','Eyeless']
chestTalentList    = ['Unbreakable','Spotter','Spark','Glasscanon','Obliterate']
backpackTalentList = ['Companion','Concussion','Vigilance']

for talent in wpnTalentList:
    print('Testing', talent , 'talent.')
    trashBuild.weaponTalent = talent
    faceTrade_simulation(trashBuild, dummyBuild, shootingRange, 1, VERBOSE)
    print('Simulation finished without errors.')

trashBuild.weaponTalent = None
for talent in chestTalentList:
    print('Testing', talent , 'talent.')
    trashBuild.chestTalent = talent
    faceTrade_simulation(trashBuild, dummyBuild, shootingRange, 1, VERBOSE)
    print('Simulation finished without errors.')

trashBuild.chestTalent = None
for talent in backpackTalentList:
    print('Testing', talent, 'talent.')
    trashBuild.backpackTalent = talent
    faceTrade_simulation(trashBuild, dummyBuild, shootingRange, 1, VERBOSE)
    print('Simulation finished without errors.')

