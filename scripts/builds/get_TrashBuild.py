from src.cfg.characterConfig import characterConfig


def get_TrashBuild():

    # Based on Savage DPS 2.0 patrick wolf build with god rolled pieces (https://www.youtube.com/watch?v=JeHD4u0gipg&t).
    # Build is 3 pc striker, 2 pc providence and Fox's prayer.
    # With some weapon handling mod because everyone know that FAL lack accuracy...
    Trashbuild = characterConfig()

    # Weapon related stats
    Trashbuild.wpn_DMG     = 23890       # FAL PvP base damage.
    Trashbuild.RPS         = 1.15*65 / 6 # 15% RPS because of 3pc striker.
    Trashbuild.MAG_size    = 41
    Trashbuild.reload_time = 2.3

    # Configure the cores. In order: Red, Blue, Yellow
    # 4 red 2 blue for the build.
    Trashbuild.nCores = [4,2,0]

    # DPS related stats
    Trashbuild.CHC  = 0.6
    Trashbuild.CHD  = 0.69
    Trashbuild.HSD  = 1.0
    Trashbuild.DTA  = 0
    Trashbuild.OoCD = 0.18
    Trashbuild.DTH  = 0.21

    # Configure the increase weapon damage and armor/health assuming god rolled items.
    Trashbuild.configure_offense()
    Trashbuild.configure_defense()

    # Configure the accuracy model.
    Trashbuild.ProbHSD = 0.75
    Trashbuild.ProbHIT = 0.75

    # Talents, exotic, specialization and some supported skills.
    Trashbuild.weaponTalent   = 'In Sync'
    Trashbuild.backpackTalent = 'Concussion'
    Trashbuild.chestTalent    = 'Spotter'
    Trashbuild.specialization = 'Technician'
    Trashbuild.useShield      = True

    return Trashbuild
