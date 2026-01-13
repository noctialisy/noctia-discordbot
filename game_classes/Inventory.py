# Class to handle inventories
import json

class Inventory:
    max_slots = 20
    items = {}

    def __init__(self, vars = None):
        if vars is None:
            self.max_slots = 20
            self.items = {
                "exp": 10,
                "gold": 0,
                "equipment": {
                    "main_weapon": "Default Weapon",
                    "sub_weapon": "",
                    "head": "",
                    "chest": "",
                    "arms": "",
                    "legs": "",
                    "necklace": ""
                },
                "pouch": []
            }

        else:
            if vars != {}:
                self.max_slots = vars['max_slots']
                self.items = vars['items']

    def print(self):
        return json.dumps({
            "max_slots": self.max_slots,
            "items": self.items
        })
    
    def get_items(self):
        return self.items
    
    def port(self, inventory):
        self.max_slots = inventory.max_slots
        self.items = inventory.items

    
