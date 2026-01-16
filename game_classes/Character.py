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
    

    # Equipment handle
    def equip_item(self, equip_type, equip_index):
        equipment = self.inventory.get_items()['equipment']
        
        if equip_type in equipment.keys():
            try:
                result = self.remove_equip(equip_type)

                if type(result) != bool:
                    raise Exception(result)

            except Exception as e:
                return e

            equip = self.inventory.items['pouch'].pop(equip_index)
            self.inventory.items['equipment'][equip_type] = equip

            self.calc_stats()
            self.save(self.entity_id)

        else:
            return "Inventory slot doesn't exist!"


    def remove_equip(self, equip_type):
        equipment = self.inventory.items['equipment']
        pouch = self.inventory.items['pouch']

        if len(pouch) >= self.inventory.get_max_slots():
            return "Inventory is full!"

        if equip_type in equipment.keys():
            equip = self.inventory.get_items()['equipment'][equip_type]

            if equip['name'] != 'Bare hands' and equip['name'] != 'Empty':
                self.inventory.items['pouch'].append(equip)

            self.inventory.items['equipment'][equip_type] = self.set_default_equip(equip_type)

            self.calc_stats()
            self.save(self.entity_id)

            return True

        else:
            return "Inventory slot doesn't exist!"
        
    def get_items(self):
        return self.inventory.get_items()