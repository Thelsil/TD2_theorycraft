from scripts.builds.get_TrashBuild import get_TrashBuild
from scripts.builds.get_optiARBuild import get_optiARBuild
from src.faceTrade_simulation import faceTrade_simulation


charCfg_main   = get_optiARBuild(5)
charCfg_target = get_TrashBuild()

simulResults = faceTrade_simulation(charCfg_main, charCfg_target, 20, 10, True)
simulResults.display()

