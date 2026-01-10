# Main entity class, it is the base for NPCs, Enemies and Characters

from .Role import Role
from .Inventory import Inventory
from .Dice import Dice


class Entity:
    RACES = ["Human", "Elf", "Catfolk", "Kitsune", "Lupine", "Orc"]
    GENDERS = ["Male", "Female"]
    STATS = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    MAX_LEVEL = 10

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        self.type = ""
        self.name = ""
        self.surname = ""
        self.gender = ""
        self.pronoun_self = ""
        self.race = ""
        self.height = ""
        self.weight = ""
        self.nsfw = False

        self.description = ""
        self.backstory = ""

        self.role = ""
        self.level = 1
        self.role_level = 1
        self.mhp=0
        self.mmp=0
        self.msp=0
        self.hp=0
        self.mp=0
        self.sp=0
        self.ac=10
        self.exp = 0
        self.req_exp = 100
        self.raw_stats = []
        self.stat_point = 0
        self.stats = {
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "luck": 0
        }
        self.skills = []
        self.abilities = []

        self.inventory = Inventory()

    
    
    # =========================================================
    # MAINS
    # =========================================================
    def describe(self):
        """
        Return the character's description
        """

        character_description = [
            self.description + "\n\n" +
            "Your stats are as follow:\n\n" +
            "Level: " + str(self.level) + "\n" +
            "HP: " + str(self.hp) + "/" + str(self.mhp) + "\n" +
            "MP: " + str(self.mp) + "/" + str(self.mmp) + "\n" +
            "SP: " + str(self.sp) + "/" + str(self.msp) + "\n" +
            "EXP: " + str(self.exp) + "/" + str(self.req_exp) + "\n\n" +
            str(self.stats)

        ]

        return character_description[0]
    
    def use_ability(self, ability_name, target):
        return self.role.use_ability(self, self.mp, self.sp, ability_name, target)    

    def check_level_up(self):
        print("current exp: " + str(self.exp))
        if self.exp >= self.req_exp:
            if self.level < self.MAX_LEVEL:
                self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.req_exp
        self.stat_point += 3
        self.calc_stats()

    def calc_stats(self):
        role_name = self.role.role_name

        if self.level == 1:
            
            if role_name == "Warrior":
                self.mhp = 12
                self.mmp = 6
                self.msp = 20

            if role_name == "Mage":
                self.mhp = 6
                self.mmp = 20
                self.msp = 12

        else:

            if role_name == "Warrior":
                self.mhp += self.roll_dice("d12")[0] + self.get_modifier('constitution')
                self.mmp += self.roll_dice("d4")[0] + self.get_modifier('intelligence')
                self.msp += self.roll_dice("d8")[0] + self.get_modifier('dexterity')

            if role_name == "Mage":
                self.mhp += self.roll_dice("d6")[0] + self.get_modifier('constitution')
                self.mmp += self.roll_dice("d12")[0] + self.get_modifier('intelligence')
                self.msp += self.roll_dice("d6")[0] + self.get_modifier('dexterity')

    def rest(self):
        self.check_level_up()

        self.hp = self.mhp
        self.mp = self.mmp
        self.sp = self.msp
    
    def roll_dice(self, dice_type):
        dice = Dice(dice_type)
        return dice.roll(1)

    # =========================================================
    # GETS
    # =========================================================
    def get_name(self):
        return self.name
    
    def get_level(self):
        return self.level
    
    def get_stats(self):
        return self.stats
    
    def get_modifier(self, stat_name: str):
        if stat_name in self.STATS:
            # Modifier = (Ability Score - 10) / 2 (rounded down
            return round((self.stats[stat_name] - 10) / 2)


    # =========================================================
    # SETS
    # =========================================================
    def set_raw_stats(self, raw_stats):
        self.raw_stats = raw_stats

    def set_stat(self, stat_value: int, character_stat: str):
        if stat_value <= self.stat_point and character_stat in self.CHARACTER_STATS:
            self.stats[character_stat] += stat_value

    def set_raw_stat(self, raw_stat_index: int, character_stat: str, empty: bool):
        if empty:
            self.raw_stats = []

        else:
            self.raw_stats.sort(reverse=True)

            if 0 <= raw_stat_index < len(self.raw_stats):
                if character_stat in self.CHARACTER_STATS:
                    self.stats[character_stat] = self.raw_stats[raw_stat_index]
    
    def set_level(self, level: int):
        self.level = level

    def set_exp(self, exp: int):
        self.exp = exp

    def set_req_exp(self, exp: int):
        self.req_exp = exp
    
    def set_role(self, role: str):
        """
        Set the character's role (class)
        
        :param role: The role to assign to the character
        :type role: str
        """
        self.role = Role(role)
        self.description = f"You are {self.name} a {self.gender} {self.race} {self.role.role_name}"