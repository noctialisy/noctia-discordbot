from .Entity import Entity
from .Role import Role
from .Inventory import Inventory
from .Dice import Dice


class Character(Entity):
    
    def __init__(self):
        super().__init__()
        self.ent_type = "Character"
        self.created = True
        self.stat_point = 0

    # =========================================================
    # MAINS
    # =========================================================
    def create(self, name: str, surname: str, race: str, gender: str, nsfw: bool):
        """
        Create a new RP character
        
        :param name: The character's name
        :type name: str
        :param surname: The character's surname
        :type surname: str
        :param race: Character's race
        :type race: str
        :param gender: Character's gender
        :type gender: str
        :param nsfw: If this character is a sfw or nsfw character
        :type nsfw: bool

        :return: Creation result
        :rtype: str
        """
        self.type = "Character"
        self.name = name
        self.surname = surname

        if race not in self.RACES:
            return "Creation Failed: Race not in scope"
        
        if gender not in self.GENDERS:
            return "Creation Failed: Gender not in scope"
        
        self.race = race
        self.gender = gender
        self.nsfw = nsfw

        if self.gender == "Female":
            self.pronoun_self = "her"
        else:
            self.pronoun_self = "his"

        self.description = f"You are {name} a {gender} {race}"

        return "Creation: success!"
    
    def has_unspent_stats(self):
        """
        Docstring for has_unspent_stats
        
        :return: True if the character has unspent stats, otherwise False
        :rtype: bool
        """
        if self.raw_stats != []:
            return True
        
        if self.stat_point > 0:
            return True
        
        return False
    

    # =========================================================
    # GETS
    # =========================================================
    def get_stat_points(self):
        return self.stat_point
    
    def get_raw_stats(self):
        return self.raw_stats
    


    # =========================================================
    # SETS
    # =========================================================
    def set_raw_stats(self, raw_stats):
        self.raw_stats = raw_stats

    def set_stat(self, stat_value: int, character_stat: str):
        if stat_value <= self.stat_point and character_stat in self.STATS:
            self.stats[character_stat] += stat_value

    def set_raw_stat(self, raw_stat_index: int, character_stat: str, empty: bool):
        if empty:
            self.raw_stats = []

        else:
            self.raw_stats.sort(reverse=True)

            if 0 <= raw_stat_index < len(self.raw_stats):
                if character_stat in self.STATS:
                    self.stats[character_stat] = self.raw_stats[raw_stat_index]

    

