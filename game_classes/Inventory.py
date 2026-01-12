# Class to handle inventories
import json

class Inventory:
    max_slots = 20
    items = []
    equipment = {}

    def __init__(self, vars = None):
        if vars is None:
            self.max_slots = 20
            self.items = []
            self.equipment = {
                "main_weapon": "Default Weapon",
                "sub_weapon": "",
                "head": "",
                "chest": "",
                "arms": "",
                "legs": "",
                "necklace": ""
            }

        else:
            if vars != {}:
                self.max_slots = vars['max_slots']
                self.max_slots = vars['max_slots']
                self.items = vars['items']
                self.equipment = vars['equipment']

    def print(self):
        return json.dumps({
            "max_slots": self.max_slots,
            "items": self.items,
            "equipment": self.equipment
        })
    
    def port(self, inventory):
        self.max_slots = inventory.max_slots
        self.items = inventory.items
        self.equipment = inventory.equipment

    
