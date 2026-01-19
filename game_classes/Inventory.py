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
                    "main_weapon": {"id": 7, "name": "Bare hands", "item_type": "weapon", "description": "", "attack_type": "melee", "dice_roll": "1d4", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}},
                    "sub_weapon": {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}},
                    "head": {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}},
                    "chest": {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}},
                    "arms": {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}},
                    "legs": {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}},
                    "necklace": {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}}
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
    
    def get_max_slots(self):
        return self.max_slots
    
    def get_items(self):
        return self.items
    
    def port(self, inventory):
        self.max_slots = inventory.max_slots
        self.items = inventory.items

    
