import random

from .Entity import Entity
from .Role import Role
from .Inventory import Inventory
from .Dice import Dice

class Enemy(Entity):
    
    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        super().__init__()
        self.ent_type = "Enemy"
        self.tag = "Common"
        self.created = True
        self.stat_point = 0

    

    # =========================================================
    # Main methods
    # =========================================================
    def create(self, name: str, race = None, gender = None, role = None, nsfw = False):
        self.ent_type = "Enemy"
        self.name = name
        self.surname = ""

        # Fills the blanks
        if race is None:
            race = random.randint(0, len(self.RACES) - 1)
            race = self.RACES[race]

        if gender is None:
            gender = random.randint(0, len(self.GENDERS) - 1)
            gender = self.GENDERS[gender]

        if role is None:
            role = random.randint(0, len(self.ROLES) - 1)
            role = self.ROLES[role]
            
            if role == 'Any':
                role = 'Warrior'

        # Check inputs
        if race not in self.RACES:
            return "Creation Failed: Race not in scope"
        
        if gender not in self.GENDERS:
            return "Creation Failed: Gender not in scope"
        
        if role not in self.ROLES:
            return "Creation Failed: Role not in scope"
        
        # Create the enemy
        self.race = race
        self.gender = gender
        self.role = self.set_role(role)
        self.nsfw = nsfw

        if self.gender == "Female":
            self.pronoun_self = "her"
        else:
            self.pronoun_self = "his"

        rolled_stats = self.roll_stats('stats')
        
        # Decide tag
        rolled_stats_sum = sum(rolled_stats)

        if rolled_stats_sum == 18:
            self.tag = "Epic Fail"
        elif rolled_stats_sum > 18 and rolled_stats_sum < 108:
            self.tag = "Common"
        elif rolled_stats_sum == 108:
            self.tag = "Legendary"

        self.description = f"{race} {role} [{self.tag}]"
        sample = random.sample([0, 1, 2, 3, 4, 5], 6)

        # ToDo: This would have to be improved by Race / Job
        self.set_raw_stat(sample[0], "strength", False)
        self.set_raw_stat(sample[1], "constitution", False)
        self.set_raw_stat(sample[2], "dexterity", False)
        self.set_raw_stat(sample[3], "wisdom", False)
        self.set_raw_stat(sample[4], "intelligence", False)
        self.set_raw_stat(sample[5], "charisma", False)
        self.set_raw_stat(0, "", True)

        self.calc_stats()
    
    def test(self):
        pass