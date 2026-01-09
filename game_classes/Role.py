# Main class for handling character roles (Mage, Warrior, Paladin, Dancer, etc.)
from .Roles.Warrior import Warrior
from .Roles.Mage import Mage

class Role:
    ROLES = ["Warrior", "Mage", "Paladin"]
    role_name = ""
    role_class = Warrior()

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self, role_name: str):
        if role_name in self.ROLES:
            self.role_name = role_name
            
            if self.role_name ==  "Warrior":
                self.role_class = Warrior()

            elif self.role_name ==  "Mage":
                self.role_class = Mage()

    def use_ability(self, entity, mp, sp, ability_name, trg_entity):
        if ability_name in self.role_class.ABILITY_NAMES:

            # Check Skill Level
            if entity.get_level() >= self.role_class.ABILITY_TREE[ability_name]['reqs']['level']:
                
                # Check resources
                if mp >= self.role_class.ABILITY_TREE[ability_name]['reqs']['mp']:
                    if sp >= self.role_class.ABILITY_TREE[ability_name]['reqs']['sp']:
                        ability_lines = self.role_class.ABILITY_TREE[ability_name]['usage_lines']

                        for key, value in ability_lines.items():
                            ability_lines[key] = str(ability_lines[key]).replace('{main_weapon}', entity.inventory.equipment["main_weapon"])
                            ability_lines[key] = str(ability_lines[key]).replace('{pronoun_self}', entity.pronoun_self)
                            ability_lines[key] = str(ability_lines[key]).replace('{target_name}', trg_entity.name)

                        # Cast the ability
                        # Attack check
                        trg_entity_ac = trg_entity.ac
                        entity_roll = entity.roll_dice("d20")[0]

                        if entity_roll > trg_entity_ac:
                            # Calc dmg
                            dmg = self.calculate_dmg(entity, trg_entity)
                            ability_lines = self.role_class.ABILITY_TREE[ability_name]['usage_lines']

                            for key, value in ability_lines.items():
                                ability_lines[key] = str(ability_lines[key]).replace('{dmg}', str(dmg))
                                ability_lines[key] = str(ability_lines[key]).replace('{dmg_type}', str('physical'))

                            return ["success", ability_lines]
                        
                        else:
                            return ["fail", ability_lines]
                    
                    else:
                        return "Lacks the required SP to use the ability"
                    
                else:
                    return "Lacks the required MP to use the ability"


            else:
                return "Your Character can't use that ability."


        else:
            return "Your Character can't use that ability."
            

        self.role_class.use_ability(ability_name)
        pass

    def calculate_dmg(self, entity, trg_entity):
        dmg = entity.roll_dice("d10")
        return dmg



