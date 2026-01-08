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
        self.level = 1
        self.role_level = 0
        self.hp=0
        self.mp=0
        self.sp=0
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
    
    def describe(self):
        """
        Return the character's description
        """

        character_description = [
            self.description + "\n\n" +
            "Your stats are as follow:\n\n" +
            "Level: " + str(self.level) + "\n" +
            "HP: " + str(self.hp) + "\n" +
            "MP: " + str(self.mp) + "\n" +
            str(self.stats)

        ]

        return character_description[0]
    
    def has_unspent_stats(self):
        """
        Docstring for has_unspent_stats
        
        :return: True if the character has unspent stats, otherwise False
        :rtype: bool
        """
        if self.raw_stats != []:
            return True
        
        if self.stat_point >= 0:
            return True
        
        return False
    
    
    # =========================================================
    # GETS
    # =========================================================
    def get_name(self):
        return self.name
    
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
        if stat_value <= self.stat_point and character_stat in self.CHARACTER_STATS:
            self.stats[character_stat] += stat_value

    def set_raw_stat(self, raw_stat_index: int, character_stat: str):
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

    

