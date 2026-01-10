# Main entity class, it is the base for NPCs, Enemies and Characters
import json

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
        self.ent_type = ""
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

        self.char_role = ""
        self.char_level = 1
        self.role_level = 1
        self.mhp=0
        self.mmp=0
        self.msp=0
        self.hp=0
        self.mp=0
        self.sp=0
        self.ac=10
        self.cur_exp = 0
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
    def load(self, vars):
        self.ent_type = vars["ent_type"]
        self.name = vars['name']
        self.surname = vars['surname']
        self.gender = vars['gender']

        if self.gender == "Female":
            self.pronoun_self = "her"
        else:
            self.pronoun_self = "his"

        self.race = vars['race']
        self.height = vars['height']
        self.weight = vars['weight']
        self.nsfw = vars['nsfw']
        self.description = vars['description']
        self.backstory = vars['backstory']
        self.char_role = Role(vars['char_role'])
        self.char_level = vars['char_level']
        self.role_level = vars['role_level']
        self.mhp = vars['mhp']
        self.mmp = vars['mmp']
        self.msp = vars['msp']
        self.hp = vars['hp']
        self.mp = vars['mp']
        self.sp = vars['sp']
        self.ac = vars['ac']
        self.cur_exp = vars['cur_exp']
        self.req_exp = vars['req_exp']
        self.raw_stats = json.loads(vars['raw_stats'])
        self.stat_point = vars['stat_point']
        self.stats = json.loads(vars['stats'])
        self.skills = json.loads(vars['skills'])
        self.abilities = json.loads(vars['abilities'])
        self.inventory = Inventory(json.loads(vars['inventory']))
    
    def describe(self):
        """
        Return the character's description
        """

        character_description = [
            self.description + "\n\n" +
            "Your stats are as follow:\n\n" +
            "Level: " + str(self.char_level) + "\n" +
            "HP: " + str(self.hp) + "/" + str(self.mhp) + "\n" +
            "MP: " + str(self.mp) + "/" + str(self.mmp) + "\n" +
            "SP: " + str(self.sp) + "/" + str(self.msp) + "\n" +
            "EXP: " + str(self.cur_exp) + "/" + str(self.req_exp) + "\n\n" +
            str(self.stats)

        ]

        return character_description[0]
    
    def use_ability(self, ability_name, target):
        return self.char_role.use_ability(self, self.mp, self.sp, ability_name, target)    

    def check_level_up(self):
        if self.cur_exp >= self.req_exp:
            if self.char_level < self.MAX_LEVEL:
                self.level_up()

    def level_up(self):
        self.char_level += 1
        self.cur_exp -= self.req_exp
        self.stat_point += 3
        self.calc_stats()

    def calc_stats(self):
        if type(self.char_role) == str:
            self.char_role = Role(self.char_role)
        
        role_name = self.char_role.role_name

        if self.char_level == 1:
            
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
        return self.char_level
    
    def get_role(self):
        return self.char_role
    
    def get_inventory(self):
        return self.inventory

    def get_stats(self):
        return self.stats
    
    def get_raw_stats(self):
        return self.raw_stats
    
    def get_skills(self):
        return self.skills
    
    def get_abilities(self):
        return self.abilities
    
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
        self.char_level = level

    def set_exp(self, exp: int):
        self.cur_exp = exp

    def set_req_exp(self, exp: int):
        self.req_exp = exp
    
    def set_role(self, role: str):
        """
        Set the character's role (class)
        
        :param role: The role to assign to the character
        :type role: str
        """
        self.char_role = Role(role)
        self.description = f"You are {self.name} a {self.gender} {self.race} {self.char_role.role_name}"

    def set_value(self, key, value):
        if key == "inventory":
            new_inventory = Inventory()
            new_inventory.port(value)
            self.inventory = new_inventory

        else:
            setattr(self, key, value)
        
        print(f"Set Character {key} to {value}")