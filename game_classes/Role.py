# Main class for handling character roles (Mage, Warrior, Paladin, Dancer, etc.)
import json, mariadb

from .GameSystem import GameSystem

class Role(GameSystem):
    ROLES = []
    role_name = ""
    role_hit_dice = ""
    role_magic_dice = ""
    role_special_dice = ""
    role_main_stat = ""
    role_sub_stat = ""
    role_abilities = []

    NO_DB_DATA_ERROR = "No data found"

    db_connection = ""
    db_cursor = ""

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self, role_name :str):
        super().__init__()

        self.ROLES = self.get_db_role_names()

        if self.ROLES == self.NO_DB_DATA_ERROR:
            print("Role class had a db fetching error!")
            self.ROLES = []

        if role_name in self.ROLES:
            self.role_name = role_name

            query = f"SELECT * FROM Roles WHERE name = '{role_name}';"
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchall()

            self.role_hit_dice = result[0]['hit_dice']
            self.role_magic_dice = result[0]['magic_dice']
            self.role_special_dice = result[0]['special_dice']
            self.role_main_stat = result[0]['main_stat']
            self.role_sub_stat = result[0]['sub_stat']
            self.role_abilities = self.get_db_role_abilities(role_name)

        else:
            print("Role class had a db fetching error!")
            self.role_name = "Not Init"

    
    # =========================================================
    # Main methods
    # =========================================================
    def use_ability(self, entity, mp, sp, ability_name, trg_entities=[]):
        ability = ''

        if type(self.role_abilities) is str:
            return "No abilities"
        
        # Attempts to find the ability
        for item in self.role_abilities:
            if item['name'] == ability_name:
                ability = item
                break

        # Check if the ability was found
        if ability == "":
            return "You don't have that ability."

        # Attempt to use the ability
        # Check ability reqs
        if entity.get_level() < ability['req_level']:
            return "You don't have that ability."
        
        if mp < ability['req_mp']:
            return "Lacks the required MP to use the ability."
        
        if sp < ability['req_sp']:
            return "Lacks the required SP to use the ability."
        
        # If no target then target self
        if type(trg_entities) is not list:
            trg_entities = [entity]
        
        # Use ability
        ability_class = ability['type'].split('_')[0]
        ability_type = ability['type'].split('_')[1]
        ability_lines = {
            "cast": ability['usage_line_cast'],
            "success": ability['usage_line_success'],
            "fail": ability['usage_line_fail']
        }
        ability_roll = ability['dice_roll']

        for key, value in ability_lines.items():
            ability_lines[key] = str(ability_lines[key]).replace('{entity_name}', entity.name)
            ability_lines[key] = str(ability_lines[key]).replace('{main_weapon}', entity.inventory.items['equipment']["main_weapon"]['name'].lower())
            ability_lines[key] = str(ability_lines[key]).replace('{pronoun_self}', entity.pronoun_self)

        calc_results = []
        action_results = []

        if ability_type == 'heal':
            # Perform Heal
            calc_results = self.calculate_heal(entity, trg_entities, ability_class, ability_roll)

        else:
            # Perform Attack
            # # Attack check [] || [result, [dmg]]
            calc_results = self.calculate_dmg(entity, trg_entities, ability_class, ability_roll)

        for result in calc_results:
            # Replace target names
            ability_lines['cast'] = str(ability_lines['cast']).replace('{target_name}', result[0])
            ability_lines['success'] = str(ability_lines['success']).replace('{target_name}', result[0])
            ability_lines['fail'] = str(ability_lines['fail']).replace('{target_name}', result[0])

            # Replace dmg type
            ability_lines['cast'] = str(ability_lines['cast']).replace('{dmg_type}', ability_type)
            ability_lines['success'] = str(ability_lines['success']).replace('{dmg_type}', ability_type)
            ability_lines['fail'] = str(ability_lines['fail']).replace('{dmg_type}', ability_type)

            # Replace heal/dmg amt
            ability_lines['cast'] = str(ability_lines['cast']).replace('{dmg}', str(result[2]))
            ability_lines['success'] = str(ability_lines['success']).replace('{dmg}', str(result[2]))
            ability_lines['fail'] = str(ability_lines['fail']).replace('{dmg}', str(result[2]))

            action_results.append([result, ability_lines])

        return action_results

    # Handle dmg
    def calculate_dmg(self, entity, entity_targets=[], ability_class="melee", ability_roll=""):
        action_results = []

        if type(entity_targets) is not list:
            # Target self if no target
            entity_targets = [entity]

        # There's an enemy entity
        if entity_targets != []:
            # Check ability class
            if ability_class == "melee":
                entity_modifier = entity.get_modifier('strength')

            elif ability_class == 'ranged' or ability_class == 'finesse':
                entity_modifier = entity.get_modifier('dexterity')

            else:
                entity_modifier = entity.get_modifier(entity.get_role().get_main_stat())

            # Calculate dmg for all targets
            for target in entity_targets:
                target_ac = target.ac
                entity_roll = entity.roll_dice('d20')[0] + entity_modifier
                print(entity.name + " Rolled Attack Check: " + str(entity_roll) + " Modifier: " + str(entity_modifier))

                if target.get_combat_ready() == 0:
                    action_results.append([target.name, 'fail_dead', 0])

                elif entity_roll >= target_ac:
                    skill_dmg_result = 0

                    # Calc ability dmg
                    if ability_roll != '':
                        ability_roll = ability_roll.split(',')
                        skill_dmg_result = 0

                        for dice in ability_roll:
                            dice_quantity = dice.split('d')[0]
                            dice_type = dice.split('d')[1]
                            skill_dmg_result += sum(entity.roll_dice('d'+dice_type, int(dice_quantity)))

                    # Calc weapon dmg
                    weap_dmg_result = 0
                    weap = entity.get_weapon()
                    weap_roll = weap['dice_roll'].split(',')

                    for dice in weap_roll:
                        dice_quantity = dice.split('d')[0]
                        dice_type = dice.split('d')[1]
                        weap_dmg_result += sum(entity.roll_dice('d'+dice_type, int(dice_quantity)))

                    # Final dmg apply
                    dmg = skill_dmg_result + weap_dmg_result + entity_modifier
                    print(entity.name + " Damaged for: " + str(dmg) + " Rolls: " + str(skill_dmg_result) + " Skill + " + str(entity_modifier) + " modifier")
                    drops = target.apply_dmg(dmg)
                    action_res_string = 'success'

                    if drops != {}:
                        entity.loot_items(drops)
                        action_res_string = 'success_win'

                    action_results.append([target.name, action_res_string, dmg])
                
                else:
                    action_results.append([target.name, 'fail', 0])

        else:
            action_results = [['empty', 'fail', [0]]]


        return action_results
    
    # Handle heals
    def calculate_heal(self, entity, entity_targets=[], ability_class="melee", ability_roll=""):
        action_results = []

        if type(entity_targets) is not list:
            # Target self if no entity provided
            entity_targets = [entity]
        
        if entity_targets != []:

            # Heal all targets
            for target in entity_targets:

                # Roll skill dmg
                skill_dmg_result = 0

                if ability_roll != '':
                    ability_roll = ability_roll.split(',')
                    skill_dmg_result = 0

                    for dice in ability_roll:
                        dice_quantity = dice.split('d')[0]
                        dice_type = dice.split('d')[1]
                        skill_dmg_result += sum(entity.roll_dice('d'+dice_type, int(dice_quantity)))

                # Check ability class
                if ability_class == "melee":
                    entity_modifier = entity.get_modifier('strength')

                elif ability_class == 'ranged' or ability_class == 'finesse':
                    entity_modifier = entity.get_modifier('dexterity')

                else:
                    entity_modifier = entity.get_modifier(entity.get_role().get_main_stat())

                # Perform Heal
                heal_amt = skill_dmg_result + entity_modifier
                print(entity.name + " Healed for: " + str(heal_amt) + " Rolls: " + str(skill_dmg_result) + " Skill + " + str(entity_modifier) + " modifier")
                target.apply_heal(heal_amt)
                action_results.append([target.name, 'success', heal_amt])

        else:
            action_results = [['empty', 'fail', [0]]]

        return action_results


    
    # =========================================================
    # Gets
    # =========================================================
    def get_name(self):
        return self.role_name
    
    def get_hit_dice(self):
        return self.role_hit_dice
    
    def get_magic_dice(self):
        return self.role_magic_dice
    
    def get_special_dice(self):
        return self.role_special_dice
    
    def get_main_stat(self):
        return self.role_main_stat
    
    def get_sub_stat(self):
        return self.role_sub_stat
    
    def get_abilities(self):
        return self.role_abilities
    
    def get_db_role_names(self):
        query = "SELECT name FROM Roles;"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            # Return the roles
            data = map(lambda row: row['name'], result)
            return list(data)

    def get_db_role_hit_dice(self, role_name):
        query = f"SELECT hit_dice FROM Roles WHERE name = \"{role_name}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            data = map(lambda row: row['hit_dice'], result)
            return list(data)[0]
        
    def get_db_role_magic_dice(self, role_name):
        query = f"SELECT magic_dice FROM Roles WHERE name = \"{role_name}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            data = map(lambda row: row['magic_dice'], result)
            return list(data)[0]
        
    def get_db_role_special_dice(self, role_name):
        query = f"SELECT special_dice FROM Roles WHERE name = \"{role_name}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            data = map(lambda row: row['special_dice'], result)
            return list(data)[0]
    
    def get_db_role_abilities(self, role_name):
        any_role = "Any"
        query = f"SELECT * FROM Abilities WHERE role_name = \"{role_name}\" OR role_name = \"{any_role}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            # Return the ability list
            return result