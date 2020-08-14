from scripts.builds.get_TrashBuild import get_TrashBuild
from scripts.tools.optimalCoreDistribution import optimalCoreDistribution


trashBuild    = get_TrashBuild()
shootingRange = 15
victoryRecord    = optimalCoreDistribution(trashBuild,shootingRange)
print(victoryRecord)

