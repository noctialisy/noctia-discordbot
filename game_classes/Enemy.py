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
        
        if type(name) is not str:
            name = 'Amelia'

        self.name = name
        self.surname = ""

        # Fills the blanks
        if race is None:
            race = self.RACES[random.randint(0, len(self.RACES) - 1)]

        if gender is None:
            gender = self.GENDERS[random.randint(0, len(self.GENDERS) - 1)]

        if role is None:
            role = self.ROLES[random.randint(0, len(self.ROLES) - 1)]
            
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
        self.nsfw = nsfw

        self.set_role(role)

        if self.gender == "Female":
            self.pronoun_self = "her"
        else:
            self.pronoun_self = "his"

        rolled_stats = self.roll_stats('stats')
        
        # Decide tag
        rolled_stats_sum = sum(rolled_stats)

        if rolled_stats_sum == 18:
            self.tag = "Epic Fail"
        elif rolled_stats_sum <= 30:
            self.tag = "Fail"
        elif rolled_stats_sum > 30 and rolled_stats_sum <= 40:
            self.tag = "Weakling"
        elif rolled_stats_sum > 40 and rolled_stats_sum <= 60:
            self.tag = "Common"
        elif rolled_stats_sum > 60 and rolled_stats_sum <= 80:
            self.tag = "Elite"
        elif rolled_stats_sum > 80 and rolled_stats_sum <= 90:
            self.tag = "Epic"
        elif rolled_stats_sum > 90 and rolled_stats_sum < 108:
            self.tag = "Legendary"
        elif rolled_stats_sum == 108:
            self.tag = "Epic Legendary"

        self.description = f"{race} {role} [{self.tag}]"

        self.assign_stat_order()
        self.calc_stats()

        return self
    
    # Pick a 2 stat preference based on Job
    def assign_stat_order(self):
        sample = random.sample([2, 3, 4, 5], 4)
        sample_index = 0
        role_main_stat = self.char_role.get_main_stat()
        role_sub_stat = self.char_role.get_sub_stat()

        for stat in self.STATS:
            if stat == 'luck':
                continue

            if stat == role_main_stat:
                stat_index = 0
            elif stat == role_sub_stat:
                stat_index = 1
            else:
                stat_index = sample[sample_index]
                sample_index += 1

            self.set_raw_stat(stat_index, stat, False)

        self.set_raw_stat(0, "", True)
    
    def test(self):
        pass