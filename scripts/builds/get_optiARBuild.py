from src.cfg.characterConfig import characterConfig


def get_optiARBuild(nBlueCores):

    # Based on cryptonomous build with god rolled pieces (https://www.youtube.com/watch?v=d6yoRms9-RI&t).
    # Build is coyote, 1 pc providence, 1pc Fenris, 1 pc ceska (or 2nd pc prov), Fox and coyote.
    # This build has slightly less HSD and more CHD than the original build.
    optiARBuild = characterConfig()

    # Weapon related stats
    optiARBuild.wpn_DMG     = 23890  # FAL PvP base damage.
    optiARBuild.RPS         = 65 / 6
    optiARBuild.MAG_size    = 41
    optiARBuild.reload_time = 2.3

    # Configure the cores. In order: Red, Blue, Yellow
    optiARBuild.nCores = [6-nBlueCores,nBlueCores,0]

    # DPS related stats
    optiARBuild.CHC  = 0.48   # CHC on coyote, ceska and fox.
    optiARBuild.CHD  = 1.63   # 25 base, 20 SHD, 10 firewall, 12 * 9 attributes.
    optiARBuild.HSD  = 1      # 45 base, 20 SHD, 15 prov, 10 from 1 attribute.
    optiARBuild.DTA  = 0.08   # 8% DTA from Contractor glove.
    optiARBuild.OoCD = 0.18   # 8 from fox, 10 from AR.
    optiARBuild.DTH  = 0.21

    # Configure the increase weapon damage and armor/health assuming god rolled items.
    optiARBuild.configure_offense(0.1) # 10% bonus WD from Fenris piece.
    optiARBuild.configure_defense()

    # Configure the accuracy model.
    optiARBuild.ProbHSD = 0.75
    optiARBuild.ProbHIT = 0.75

    # Talents, exotic, specialization and some supported skills.
    optiARBuild.weaponTalent   = 'In Sync'
    optiARBuild.backpackTalent = 'Concussion'
    optiARBuild.chestTalent    = 'Unbreakable'
    optiARBuild.exoticPiece    = 'Coyote'
    optiARBuild.specialization = 'Firewall'
    optiARBuild.useShield      = True

    return optiARBuild
