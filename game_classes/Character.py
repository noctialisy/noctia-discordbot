from .Inventory import Inventory

class Character:
    CHARACTER_RACES = ["Human", "Elf", "Catfolk", "Kitsune", "Lupine"]
    CHARACTER_GENDERS = ["Male", "Female"]
    CHARACTER_STATS = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

    def __init__(self):
        self.name = ""
        self.surname = ""
        self.gender = ""
        self.race = ""
        self.height = ""
        self.weight = ""
        self.nsfw = False

        self.description = ""
        self.backstory = ""

        self.role = ""
        self.level = 0
        self.role_level = 0
        self.hp=0
        self.mp=0
        self.sp=0
        self.raw_stats = []
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
        self.name = name
        self.surname = surname

        if race not in self.CHARACTER_RACES:
            return "Creation Failed: Race not in scope"
        
        if gender not in self.CHARACTER_GENDERS:
            return "Creation Failed: Gender not in scope"
        
        self.race = race
        self.gender = gender
        self.nsfw = nsfw

        self.description = f"You are {name} a {gender} {race}"

        return "Creation: success!"
    
    def get_name(self):
        return self.name
    
    def set_raw_stats(self, raw_stats):
        self.raw_stats = raw_stats

    def assign_raw_stat(self, raw_stat_index: int, character_stat: str):
        if 0 < raw_stat_index < len(self.raw_stats):
            if character_stat in self.CHARACTER_STATS:
                self.stats[character_stat] = self.raw_stats[raw_stat_index]
                self.raw_stats.pop(raw_stat_index)
    
    def set_role(self, role: str):
        """
        Set the character's role (class)
        
        :param role: The role to assign to the character
        :type role: str
        """
        self.role = role
    
    def describe(self):
        """
        Return the character's description
        """
        return self.description

    

