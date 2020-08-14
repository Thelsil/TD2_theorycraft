import numpy as np


class characterConfig:

    ################################################
    #               PUBLIC ATTRIBUTES              #
    ################################################

    # Weapon related stats
    wpn_DMG     = None # PvP BASE damage of the weapon! Without any weapon damage increase!
    MAG_size    = None # Magazine size of the weapon.
    reload_time = None # Reload time of the weapon.
    RPS         = None # Round Per Second of the weapon (= RPM/60)
    weaponType  = 'AR' # Weapon type. 'AR', 'LMG', 'Rifle', 'MMR', 'SMG', 'Shotgun', 'Pistol'

    # Core configuration. In order: Red, Blue, Yellow
    nCores = [0,0,0]

    # DPS related stats
    IWD  = None # Increase weapon damage as it is shown in the in-game character stats.
    DTA  = 0    # Damage to Armor as it is shown in the in-game character stats.
    DTH  = 0    # Damage to Health as it is shown in the in-game character stats.
    OoCD = 0    # Out of Cover Damage as it is shown in the in-game character stats.
    CHC  = None # Critical Hit Chance as it is shown in the in-game character stats.
    CHD  = None # Critical Hit Damages as it is shown in the in-game character stats.
    HSD  = None # Headshot Shot Damages as it is shown in the in-game character stats.

    # Accuracy setup.
    ProbHIT = 1    # Probability of hitting shoots.
    ProbHSD = 0.25 # Probability of hitting headshoots.

    # defensive stats
    armor = None
    health = None

    # Talents, exotic, specialization and some supported skills.
    weaponTalent   = None
    backpackTalent = None
    chestTalent    = None
    exoticPiece    = None
    specialization = None
    useShield      = False

    # For simulation purpose only.
    init_ATB = 0

    ################################################
    #              PRIVATE ATTRIBUTES              #
    ################################################

    __range = 10

    # COOLDOWN MANAGEMENT
    __weaponTimer = None
    __weaponCD = None
    __backpackTimer = None
    __backpackCD = None
    __chestTimer = None
    __chestCD = None

    __currMAG = None
    __currArmor = None
    __currHealth = None
    __currBonusArmor = None  # For later implementations.
    __unbreakableON = False

    __currShieldHealth = None

    __shieldHealth_base = 1327245
    __ShieldST_healthModified = [1.13, 1.53, 1.79, 2.13, 2.63, 3.13, 3.63]

    ################################################
    #                 PUBLIC METHODS               #
    ################################################

    def hasArmor(self):
        if 0 < self.__currArmor:
            return True
        else:
            return False

    def effectiveHitPoints(self):
        return [self.__currArmor, self.__currHealth, self.__currShieldHealth]

    def shoot(self, hasArmor=True, hasShield=False):

        if self.__currMAG < 1:
            return 0

        if self.isDead():
            return 0

        self.__currMAG -= 1

        # Define all RNG rolls.
        critRoll = np.random.random()
        hitRoll = np.random.random()
        HSDRoll = np.random.random()

        # Calculate base damage.
        totalWpnDMG = self.__getTotalWpnDmg()
        incrWpnDMG = self.__getIncrWpnDmg()
        ampWpnDMG = self.__getAmpWpnDmg()
        base_DMG = self.wpn_DMG * (1 + incrWpnDMG) * (1 + totalWpnDMG) * (1 + self.OoCD) * ampWpnDMG

        if hitRoll <= self.ProbHIT:
            hitm = 1
        else:
            hitm = 0

        if HSDRoll <= self.ProbHSD:
            hsdm = 1
            if self.backpackTalent == 'Concussion':
                self.__backpackTimer = 0
        else:
            hsdm = 0

        # Consider damage to health or damage to armor for base dmg calculation
        if hasShield:
            if hsdm == 1:
                if hasArmor:
                    base_DMG *= (1 + self.DTA)
                else:
                    base_DMG *= (1 + self.DTH)
        else:
            if hasArmor:
                base_DMG *= (1 + self.DTA)
            else:
                base_DMG *= (1 + self.DTH)

        currCHC = self.__getCurrCHC()
        if critRoll < currCHC:
            currCHD = self.__getCurrCHD()
            DMG = base_DMG * (1 + currCHD + hsdm * self.HSD) * hitm

            if self.chestTalent == 'Obliterate':
                if len(self.__chestTimer) < 15:
                    self.__chestTimer.append(0)

        else:
            DMG = base_DMG * hitm * (1 + hsdm * self.HSD)

        return [DMG, hsdm]

    def init(self, shootingRange=15):
        self.__currMAG = self.MAG_size
        self.__currHealth = self.health
        self.__currArmor = self.armor
        self.__range = shootingRange

        if self.chestTalent == 'Unbreakable':
            self.__unbreakableON = True
        else:
            self.__unbreakableON = False

        self.__initCooldown()

        if self.useShield:
            shield_ST = self.nCores[1] + self.nCores[2]
            if self.specialization == 'Technician':
                shield_ST += 1

            if 6 < shield_ST:
                shield_ST = 6

            self.__currShieldHealth = self.__shieldHealth_base * self.__ShieldST_healthModified[shield_ST]
        else:
            self.__currShieldHealth = 0


    def isEmptyMag(self):
        if self.__currMAG == 0:
            return True
        else:
            return False

    def shieldDeployed(self):
        if 0 < self.__currShieldHealth:
            return True
        else:
            return False

    def reload(self):
        self.__currMAG = self.MAG_size
        if self.weaponTalent == 'Strained':
            self.__weaponTimer = 0

    def damage(self, val, verbose=''):

        DMG = val[0]
        hsdm = val[1]

        # Multiply damage if glasscanon is used.
        if self.chestTalent == 'Glasscanon':
            DMG *= 1.5

        if DMG == 0:
            if verbose != '':
                print(verbose, ' opponent missed!')
            return

        if 0 < self.__currShieldHealth and hsdm == 0:

            if self.chestTalent == 'Vanguard' and self.__chestTimer < self.__chestCD:
                if verbose != '':
                    print(verbose, ' takes no shield damages thanks to Vanguard!.')
                return

            self.__currShieldHealth -= 3 * DMG

            if verbose != '':
                print(verbose, ' takes ', str(3 * DMG), ' shield damages.')
            return

        if self.backpackTalent == 'Vigilance':
            self.__backpackTimer = 0

        if 0 < self.__currArmor:

            if verbose != '':
                if hsdm == 1:
                    print('Headshot! ', verbose, ' takes ', str(DMG), ' armor damages.')
                else:
                    print(verbose, ' takes ', str(DMG), ' armor damages.')

            self.__currArmor -= DMG
            if self.__currArmor < 0:
                self.__currHealth += self.__currArmor

                if self.__unbreakableON:
                    if verbose != '':
                        print(verbose, ' unbreakable activated!')
                    self.__unbreakableON = False
                    self.__currArmor = self.armor / 2

        else:

            if verbose != '':
                if hsdm == 1:
                    print('Headshot! ', verbose, ' takes ', str(DMG), ' health damages.')
                else:
                    print(verbose, ' takes ', str(DMG), ' health damages.')

            self.__currHealth -= DMG

    def isDead(self):
        if self.__currHealth <= 0:
            return True
        else:
            return False


    def copy(self, charCfg):

        # Copy weapon related stats
        self.wpn_DMG = charCfg.wpn_DMG
        self.RPS = charCfg.RPS
        self.MAG_size = charCfg.MAG_size
        self.reload_time = charCfg.reload_time
        self.weaponType = charCfg.weaponType

        # Copy core config.
        self.nCores = charCfg.nCores

        # copy DPS related stats
        self.IWD = charCfg.IWD
        self.DTA = charCfg.DTA
        self.DTH = charCfg.DTH
        self.OoCD = charCfg.OoCD
        self.CHC = charCfg.CHC
        self.CHD = charCfg.CHD
        self.HSD = charCfg.HSD

        # Copy accuracy setup.
        self.ProbHIT = charCfg.ProbHIT
        self.ProbHSD = charCfg.ProbHSD

        # copy defensive stats
        self.armor = charCfg.armor
        self.health = charCfg.health

        # Copy Talents, exotic, pecialization and some supported skills.
        self.weaponTalent = charCfg.weaponTalent
        self.chestTalent = charCfg.chestTalent
        self.backpackTalent = charCfg.backpackTalent
        self.specialization = charCfg.specialization
        self.useShield = charCfg.useShield
        self.init_ATB = charCfg.init_ATB

    def getCurrArmor(self):
        return self.__currArmor

    def updateCooldown(self, time):

        if self.backpackTalent == 'Vigilance':
            if self.__backpackTimer < self.__backpackCD:
                self.__backpackTimer += time

        if self.chestTalent == 'Vanguard':
            self.__chestTimer += time

        if self.weaponTalent == 'Strained':
            self.__weaponTimer += time

        if self.backpackTalent == 'Concussion':
            if self.__backpackTimer < self.__backpackCD:
                self.__backpackTimer += time

        if self.chestTalent == 'Obliterate':

            oldTimer = self.__chestTimer
            self.__chestTimer = []
            for i in range(len(oldTimer)):
                newTimer = oldTimer[i] + time
                if newTimer < self.__chestCD:
                    self.__chestTimer.append(newTimer)

    def configure_defense(self, incrArmor=0, incrHealth=0):
        self.armor = (660 + 170 * self.nCores[1]) * (1.1 + incrArmor) * 1000
        self.health = 300000 * (1.1 + incrHealth)

    def configure_offense(self, bonusIWD=0):
        # 0.1 SHD, 0.15 weapon dmg, 0.7 from spec = 0.32 base.
        self.IWD = 0.32 + bonusIWD + 0.15 * self.nCores[0]

    ################################################
    #                 PRIVATE METHODS              #
    ################################################

    def __initCooldown(self):

        if self.backpackTalent == 'Vigilance':
            self.__backpackCD = 4
            self.__backpackTimer = 4

        if self.chestTalent == 'Vanguard':
            self.__chestTimer = 0
            self.__chestCD = 2

        if self.weaponTalent == 'Strained':
            self.__weaponTimer = 0

        if self.backpackTalent == 'Concussion':
            if self.weaponType == 'MMR':
                self.__backpackCD = 5
            else:
                self.__backpackCD = 1.5
            self.__backpackTimer = 10

        if self.chestTalent == 'Obliterate':
            self.__chestCD = 5
            self.__chestTimer = []

    def __getIncrWpnDmg(self):

        incrWpnDMG = self.IWD
        if self.weaponTalent == 'In Sync':
            incrWpnDMG += 0.3

        if self.weaponTalent == 'Ignited' or self.weaponTalent == 'Eyeless' or self.weaponTalent == 'Sadistic':
            incrWpnDMG += 0.2

        if self.weaponTalent == 'Optimist':
            incrWpnDMG += 0.3 * self.__currMAG / self.MAG_size

        return incrWpnDMG

    def __getCurrCHC(self):
        currCHC = self.CHC

        if self.exoticPiece == 'Coyote':
            if 15 <= self.__range < 25:
                currCHC += 0.10

            if 25 <= self.__range:
                currCHC += 0.25

        return currCHC

    def __getCurrCHD(self):
        currCHD = self.CHD
        if self.weaponTalent == 'Strained':
            nStacks = np.minimum(np.floor(2 * self.__weaponTimer), 5)
            currCHD = currCHD + 0.1 * nStacks

        if self.exoticPiece == 'Coyote':
            if self.__range <= 15:
                currCHD += 0.25
            if 15 < self.__range < 25:
                currCHD += 0.10

        return currCHD

    def __getTotalWpnDmg(self):
        totalWpnDMG = 0
        if self.backpackTalent == 'Vigilance':
            if self.__backpackCD <= self.__backpackTimer:
                totalWpnDMG += 0.25

        if self.backpackTalent == 'Wicked':
            totalWpnDMG += 0.18

        if self.chestTalent == 'Obliterate':
            totalWpnDMG += 0.01 * len(self.__chestTimer)

        if self.chestTalent == 'Spark':
            totalWpnDMG += 0.15

        if self.backpackTalent == 'Companion':
            totalWpnDMG += 0.15

        if self.backpackTalent == 'Concussion':
            if self.__backpackTimer < self.__backpackCD:
                totalWpnDMG += 0.1

        return totalWpnDMG

    def __getAmpWpnDmg(self):
        AmpWpnDMG = 1

        if self.chestTalent == 'Spotter':
            AmpWpnDMG *= 1.15

        if self.chestTalent == 'Glasscanon':
            AmpWpnDMG *= 1.25

        if self.chestTalent == 'Perfect Glasscanon':
            AmpWpnDMG *= 1.3

        if self.specialization == 'Firewall':
            if self.shieldDeployed() and self.__range <= 10:
                AmpWpnDMG *= 1.11

        return AmpWpnDMG
