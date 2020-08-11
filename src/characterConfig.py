import numpy as np

class characterConfig:

    # DPS stats
    base_DMG    = None
    CHC         = None
    CHD         = None
    RPS         = None
    HSD         = None
    MAG_size    = None
    reload_time = None
    ProbHIT     = 1
    ProbHSD     = 0.25
    shield_ST   = -1

    # eHP stats
    armor  = None
    health = None

    # Talents
    hasUnbreakable = False


    ## PRIVATE
    __currMAG          = None
    __currArmor        = None
    __currHealth       = None
    __unbreakableON    = False
    __currShieldHealth = None

    __shieldHealth_base       = 1327245
    __ShieldST_healthModified = [1.13,1.53,1.79,2.13,2.63,3.13,3.63]


    nSimulSamples   = 10**6
    maxSavedBullets = 75


    def get_bustDPS(self):

        bDPS = self.base_DMG*(1+self.CHC*self.CHD+self.ProbHSD*self.HSD)*self.RPS*self.ProbHIT
        return bDPS

    def get_substainDPS(self):

        sDPS    = self.get_bustDPS()
        T_shoot = self.MAG_size/self.RPS
        sDPS = sDPS*T_shoot/(T_shoot+self.reload_time)
        return sDPS

    def shoot(self):

        if self.__currMAG < 1:
            return 0

        if self.isDead():
            return 0

        self.__currMAG -= 1

        critRoll = np.random.random()
        hitRoll = np.random.random()
        HSDRoll = np.random.random()

        if (hitRoll < self.ProbHIT):
            hitm = 1
        else:
            hitm = 0

        if (HSDRoll < self.ProbHSD):
            hsdm = 1
        else:
            hsdm = 0

        if (critRoll < self.CHC):
            DMG = self.base_DMG * (1 + self.CHD + hsdm * self.HSD) * hitm
        else:
            DMG = self.base_DMG * hitm * (1 + hsdm * self.HSD)

        return [DMG,hsdm]

    def reset(self):
        self.__currMAG          = self.MAG_size
        self.__currHealth       = self.health
        self.__currArmor        = self.armor
        self.__unbreakableON    = self.hasUnbreakable
        if(self.shield_ST < 0):
            self.__currShieldHealth = 0
        else:
            self.__currShieldHealth = self.__shieldHealth_base*self.__ShieldST_healthModified[self.shield_ST]

    def isEmptyMag(self):
        if(self.__currMAG == 0):
            return True
        else:
            return False

    def reload(self):
        self.__currMAG = self.MAG_size

    def damage(self,val):

        DMG  = val[0]
        hsdm = val[1]
        if( 0 < self.__currShieldHealth and hsdm == 0 ):
            self.__currShieldHealth -= 3*DMG
            return

        if( 0 < self.__currArmor):

            self.__currArmor -= DMG
            if (self.__currArmor < 0):
                self.__currHealth += self.__currArmor

                if(self.__unbreakableON):
                    self.__unbrakableON = False
                    self.__currArmor    = self.armor/2

        else:

            self.__currHealth -= DMG

    def isDead(self):
        if(self.__currHealth <= 0):
            return True
        else:
            return False


    def copy(self,charCfg):
        self.base_DMG = charCfg.base_DMG
        self.CHC = charCfg.CHC
        self.CHD = charCfg.CHD
        self.RPS = charCfg.RPS
        self.HSD = charCfg.HSD
        self.MAG_size = charCfg.MAG_size
        self.reload_time = charCfg.reload_time
        self.ProbHIT = charCfg.ProbHIT
        self.ProbHSD = charCfg.ProbHSD
        self.armor = charCfg.armor
        self.health = charCfg.health
        self.hasUnbreakable = charCfg.hasUnbreakable
        self.shield_ST      = charCfg.shield_ST

    def getCurrArmor(self):
        return self.__currArmor


    def configure_defense(self,nCores,useShield = True,incrArmor = 0,incrHealth = 0):
        self.armor     = (660 +  170 * nCores)*(1.1 + incrArmor)*1000
        if useShield:
            self.shield_ST = nCores
        else:
            self.shield_ST = -1
        self.health    = 300000*(1.1+incrHealth)