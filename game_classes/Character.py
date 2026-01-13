# Handle the characters

from .Entity import Entity
from .Role import Role
from .Inventory import Inventory
from .Dice import Dice


class Character(Entity):
    
    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        super().__init__()
        #print("Init Character")
        self.ent_type = "Character"
        self.created = True
        self.stat_point = 0

    
    
    # =========================================================
    # Main methods
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
        self.ent_type = "Character"
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
    