# Main entity class, it is the base for NPCs, Enemies and Characters
import os, json, pickle, random

from .GameSystem import GameSystem
from .Role import Role
from .Inventory import Inventory
from .Dice import Dice

class Entity(GameSystem):
    
    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        super().__init__()
        #print("Init Entity")
        self.entity_id = ""
        self.ent_type = ""
        self.name = ""
        self.surname = ""
        self.gender = ""
        self.pronoun_self = ""
        self.race = ""
        self.height = 0
        self.weight = 0
        self.nsfw = False

        self.description = ""
        self.backstory = ""

        self.char_role = "Warrior"
        self.char_level = 1
        self.role_level = 1
        self.mhp=0
        self.mmp=0
        self.msp=0
        self.hp=0
        self.mp=0
        self.sp=0
        self.ac=10
        self.cur_exp = 0
        self.req_exp = 300
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
        self.inventory = Inventory()

        self.combat_ready = 1
        self.combat_claims = []
    
    
    
    # =========================================================
    # MAINS
    # =========================================================
    def load(self, user_id: str):
        """
        Load the character from the database, can also check for existence
        
        :param user_id: Specify the user reference id for the character to load
        :type user_id: int

        :return: Character loaded if load ok, otherwise str
        :rtype: Character
        """

        ent_type = self.ent_type

        if type(user_id) is not str:
            user_id = str(user_id)

        if ent_type == 'Character':
            if not user_id.startswith('@'):
                user_id = '@' + user_id

        # Search for the character in the db
        query = f"SELECT id FROM Entities WHERE uid = '{user_id}';"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if len(result) == 0:
            # No char found
            # Try user file
            return self.NO_CHARACTER_FOUND_ERROR
            
        else:
            query = f"SELECT * from Entities WHERE uid = '{user_id}';"
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchall()

            self.load_data(result[0])

            return self

    def save(self, save_method = "db"):
        """
        Save the character to the database
        
        :param user_id: Specify the user reference id for the character to save
        :type user_id: int
        :param character: The character to save
        :type character: Character
        """

        user_id = self.entity_id
        ent_type = self.ent_type

        if ent_type == 'Character':
            if not user_id.startswith('@'):
                user_id = '@' + user_id + ''

        if save_method == "file":
            with open('./game_saves/character_'+str(user_id)+'.pickle', 'wb') as file:
                pickle.dump(self, file)

        else:
            #print(f"Saving character {user_id}...")
            # Search for the character in the db
            query = f"SELECT id from Entities WHERE uid = '{str(user_id)}';"
            self.db_cursor.execute(query)
            query_res = self.db_cursor.fetchall()

            # Must transform the data because vars() returns a pointer to the class values
            self.entity_id = user_id
            save_data = {}
            data = vars(self)

            for key in data.keys():
                attr_value = getattr(self, key)
                save_data[key] = attr_value

            save_data["uid"] = user_id
            save_data['char_role'] = self.get_role().role_name
            save_data['raw_stats'] = json.dumps(self.get_raw_stats())
            save_data['stats'] = json.dumps(self.get_stats())
            save_data['skills'] = json.dumps(self.get_skills())
            save_data['abilities'] = json.dumps(self.get_abilities())
            save_data['inventory'] = self.get_inventory().print()
            save_data['combat_claims'] = json.dumps(self.get_combat_claims())

            if save_data['height'] == "":
                save_data['height'] = 0
            
            if save_data['weight'] == "":
                save_data['weight'] = 0

            if query_res == []:
                # No char found in DB, Insert
                query = ("INSERT INTO `Entities` "
                            "(uid, ent_type, name, surname, gender, race, height, weight, nsfw, description, backstory, char_role, char_level, role_level, mhp, mmp, msp, hp, mp, sp, ac, cur_exp, req_exp, raw_stats, stat_point, stats, skills, inventory, combat_ready, combat_claims) "
                            f"VALUES(\"{save_data['uid']}\", \"{save_data['ent_type']}\", \"{save_data['name']}\", \"{save_data['surname']}\", \"{save_data['gender']}\", \"{save_data['race']}\", {int(save_data['height'])}, {int(save_data['weight'])}, "
                            f"{int(save_data['nsfw'])}, \"{save_data['description']}\", \"{save_data['backstory']}\", \"{save_data['char_role']}\", {save_data['char_level']}, "
                            f"{save_data['role_level']}, {save_data['mhp']}, {save_data['mmp']}, {save_data['msp']}, {save_data['hp']}, {save_data['mp']}, {save_data['sp']}, {save_data['ac']}, "
                            f"{save_data['cur_exp']}, {save_data['req_exp']}, '{save_data['raw_stats']}', {save_data['stat_point']}, '{save_data['stats']}', '{save_data['skills']}', '{save_data['inventory']}', {save_data['combat_ready']}, '{save_data['combat_claims']}');")

            else:
                # Char exists, Update
                query = (f"UPDATE `Entities` SET "
                            f"name = \"{save_data['name']}\", surname = \"{save_data['surname']}\", gender = \"{save_data['gender']}\", race = \"{save_data['race']}\", "
                            f"height = {int(save_data['height'])}, weight = {int(save_data['weight'])}, nsfw = {int(save_data['nsfw'])}, description = \"{save_data['description']}\", backstory = \"{save_data['backstory']}\", "
                            f"char_role = \"{save_data['char_role']}\", char_level = {save_data['char_level']}, role_level = {save_data['role_level']}, "
                            f"mhp = {save_data['mhp']}, mmp = {save_data['mmp']}, msp = {save_data['msp']}, hp = {save_data['hp']}, mp = {save_data['mp']}, sp = {save_data['sp']}, ac = {save_data['ac']}, "
                            f"cur_exp = {save_data['cur_exp']}, req_exp = {save_data['req_exp']}, "
                            f"raw_stats = '{save_data['raw_stats']}', stat_point = {save_data['stat_point']}, stats = '{save_data['stats']}', "
                            f"skills = '{save_data['skills']}', inventory = '{save_data['inventory']}', combat_ready = {save_data['combat_ready']}, combat_claims = '{save_data['combat_claims']}' "
                            f"WHERE uid = \"{save_data['uid']}\";")
            

            self.db_cursor.execute(query)

    def load_data(self, vars):
        self.entity_id = vars['uid']
        self.ent_type = vars["ent_type"]
        self.name = vars['name']
        self.surname = vars['surname']
        self.gender = vars['gender']

        if self.gender == "Female":
            self.pronoun_self = "her"
        else:
            self.pronoun_self = "his"

        self.race = vars['race']
        self.height = vars['height']
        self.weight = vars['weight']
        self.nsfw = vars['nsfw']
        self.description = vars['description']
        self.backstory = vars['backstory']
        self.char_role = Role(vars['char_role'])
        self.char_level = vars['char_level']
        self.role_level = vars['role_level']
        self.mhp = vars['mhp']
        self.mmp = vars['mmp']
        self.msp = vars['msp']
        self.hp = vars['hp']
        self.mp = vars['mp']
        self.sp = vars['sp']
        self.ac = vars['ac']
        self.cur_exp = vars['cur_exp']
        self.req_exp = vars['req_exp']
        self.stat_point = vars['stat_point']
        self.raw_stats = json.loads(vars['raw_stats'])
        self.stats = json.loads(vars['stats'])
        self.skills = json.loads(vars['skills'])
        self.inventory = Inventory(json.loads(vars['inventory']))
        self.combat_ready = vars['combat_ready']
        self.combat_claims = json.loads(vars['combat_claims'])
    
    def delete(self, user_id: int):
        user_id = self.entity_id
        ent_type = self.ent_type

        if ent_type == 'Character':
            if not user_id.startswith('@'):
                user_id = '@' + user_id + ''

        # Search for the character in the db
        query = f"SELECT id from Entities WHERE ent_type = '{ent_type}' AND uid = '{user_id}';"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result != []:
            query_del = (f"DELETE FROM `Entities` WHERE ent_type = '{ent_type}' AND uid = '{user_id}';")
            self.db_cursor.execute(query_del)

    def describe(self):
        """
        Return the character's description
        """

        character_description = [
            self.description + "\n\n" +
            "Your stats are as follow:\n\n" +
            "Level: " + str(self.char_level) + "\n" +
            "HP: " + str(self.hp) + "/" + str(self.mhp) + "\n" +
            "EXP: " + str(self.cur_exp) + "/" + str(self.req_exp) + "\n\n" +
            str(self.stats)

        ]

        return character_description[0]
    
    def use_ability(self, ability_name = None, targets=[]):
        if self.combat_ready == 0:
            return "was defeated in this battle and needs to recover"

        if self.ent_type == 'Enemy' and ability_name is None:
            abilities = []

            for ability in self.get_abilities():
                if ability['name'] == 'Defend':
                    continue
                if ability['name'] == 'Pat':
                    continue

                abilities.append(ability)

            random_index = random.randint(0, len(abilities) - 1)
            ability = abilities[random_index]
            ability_name = ability['name']

        if type(targets) is not list:
            if targets is not None:
                targets = [targets]

            else:
                targets = []

        return self.char_role.use_ability(self, self.mp, self.sp, ability_name, targets)    

    def check_level_up(self, force = False):
        leveled = False

        if self.cur_exp >= self.req_exp and self.cur_exp != 0 or force:
            if self.char_level < self.MAX_LEVEL:
                self.level_up()
                self.calc_stats()
                leveled = True
        
        return leveled

    def level_up(self):
        self.cur_exp -= self.req_exp

        if self.cur_exp < 0:
            self.cur_exp = 0

        self.char_level += 1
        self.req_exp += (self.req_exp * 2)
        self.stat_point += 3

    def calc_stats(self):
        if type(self.char_role) == str:
            self.char_role = Role(self.char_role)
        
        # Get specific dices for the Role
        hit_dice = self.char_role.role_hit_dice
        magic_dice = self.char_role.role_magic_dice
        special_dice = self.char_role.role_special_dice

        if self.char_level == 1:
            # At start, Max dice + modifier
            self.mhp = max(1, int(hit_dice.split("d")[1]) + self.get_modifier('constitution'))
            self.mmp = max(1, int(magic_dice.split("d")[1]) + self.get_modifier('intelligence'))
            self.msp = max(1, int(special_dice.split("d")[1]) + self.get_modifier('dexterity'))

            # Calculate base AC
            self.ac = 10 + self.get_modifier('constitution')

        else:
            # Lv2+, dice_roll + modifier
            self.mhp += max(0, self.roll_dice(hit_dice)[0] + self.get_modifier('constitution'))
            self.mmp += max(0, self.roll_dice(magic_dice)[0] + self.get_modifier('intelligence'))
            self.msp += max(0, self.roll_dice(special_dice)[0] + self.get_modifier('dexterity'))

            # Calculate base AC
            self.ac = 10 + self.get_modifier('constitution')

    def rest(self):
        self.check_level_up()
        self.hp = self.mhp
        self.mp = self.mmp
        self.sp = self.msp
        self.combat_ready = 1
    
    def apply_dmg(self, dmg_amt):
        drops = {}

        if self.hp >= dmg_amt:
            self.hp = self.hp - dmg_amt
        else:
            self.hp = 0

        # Calc and process drops
        if self.hp == 0:
            self.combat_ready = 0

            for tmp_entity_id in self.combat_claims:
                # Recalculate the drops for every "party" member
                drops = self.drop_items()

                tmp_entity_id = str(tmp_entity_id)
                tmp_entity = Entity()

                if tmp_entity_id.startswith('@'):
                    tmp_entity.ent_type = 'Character'

                else:
                    tmp_entity.ent_type = 'Enemy'

                tmp_entity = tmp_entity.load(tmp_entity_id)
                tmp_entity.loot_items(drops)
                tmp_entity.save()

            if self.ent_type == "Character":
                self.save(self.entity_id)

            if self.ent_type == "Enemy":
                self.delete(self.entity_id)

        else:
            self.save(self.entity_id)


        return drops

    def apply_heal(self, heal_amt):
        total_hp_after_heal = self.hp + heal_amt

        if total_hp_after_heal > self.mhp:
            self.hp = self.mhp
        else:
            self.hp = total_hp_after_heal

        self.save(self.entity_id)

    def revive(self):
        heal = 0

        if self.combat_ready == 0:
            heal = int(self.mhp * 0.20)
            self.hp = heal
            self.combat_ready = 1
            self.save()

        return heal
    
    def drop_items(self):
        inventory = self.inventory.get_items()

        drops = {
            "exp": 0,
            "gold": 0,
            "equipment": [],
            "pouch": []
        }

        if self.ent_type == "Enemy":
            drops['exp'] = inventory['exp']
            drops['gold'] = inventory['gold']
        
        else:
            roll_for_gold = self.roll_dice("d100")
            roll_for_exp = self.roll_dice("d100")

            # These would need to be checked for actual drop chances in DB
            if roll_for_exp[0] <= 10:
                drops['exp'] = inventory['exp']

            if roll_for_gold[0] <= 20:
                drops['gold'] = inventory['gold']

        # Roll for item loss
        for key, item in enumerate(inventory['pouch']):
            item_drop_chance = item['base_drop_rate'] * 100
            roll = self.roll_dice('d100')

            if roll[0] <= item_drop_chance:
                drops['pouch'].append(inventory['pouch'].pop(key))


        # Roll for equip loss
        for key, equip in inventory['equipment'].items():
            equip_drop_chance = equip['base_drop_rate'] * 100
            roll = self.roll_dice('d100')

            if roll[0] <= equip_drop_chance:
                drops['equipment'].append(equip)
                self.remove_equip(key, delete=True)


        return drops

    def loot_items(self, items: dict):
        if type(items) is not dict:
            items = {}

        for key, item in items.items():
            if key == "exp":
                self.set_exp(int(item))

            elif key == "gold":
                self.inventory.items["gold"] += item

            elif key == "pouch":
                if len(self.inventory.items['pouch']) < self.inventory.get_max_slots():
                    for i in item:
                        self.inventory.items['pouch'].append(i)

            elif key == "equipment":
                if len(self.inventory.items['pouch']) < self.inventory.get_max_slots():
                    for i in item:
                        self.inventory.items['pouch'].append(i)
        
        self.save(self.entity_id)
    
    def roll_stats(self, result_type='text'):
        dice = Dice("d6")
        roll = 0
        results = []
        result_values = []

        while roll < 6:
            rolled = dice.roll(4)
            result = sum(sorted(rolled)[-3:])
            results.append(str(rolled) + "(" + str(result) + ")")
            result_values.append(result)

            roll += 1

        result_values.sort(reverse=True)
        self.set_raw_stats(result_values)

        if result_type == 'text':
            return results
        else:
            return result_values
    
    def roll_dice(self, dice_type, quantity=1):
        dice = Dice(dice_type)
        return dice.roll(quantity)

    def has_unspent_stats(self):
        """
        Docstring for has_unspent_stats
        
        :return: True if the character has unspent stats, otherwise False
        :rtype: bool
        """
        
        if len(self.raw_stats) > 0:
            return True
        
        if self.stat_point > 0:
            return True
        
        return False
    
    def add_combat_claim(self, entity_id):
        if entity_id not in self.combat_claims:
            self.combat_claims.append(entity_id)
            self.save()

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

    def remove_equip(self, equip_type, delete = False):
        equipment = self.inventory.items['equipment']
        pouch = self.inventory.items['pouch']

        if len(pouch) >= self.inventory.get_max_slots():
            return "Inventory is full!"

        if equip_type in equipment.keys():
            equip = self.inventory.get_items()['equipment'][equip_type]

            if equip['name'] != 'Bare hands' and equip['name'] != 'Empty':
                if delete == False:
                    self.inventory.items['pouch'].append(equip)

            self.set_default_equip(equip_type)
            self.calc_stats()
            self.save(self.entity_id)

            return True

        else:
            return "Inventory slot doesn't exist!"

    # =========================================================
    # GETS
    # =========================================================
    def get_id(self):
        return self.entity_id

    def get_name(self):
        return self.name
    
    def get_level(self):
        return self.char_level
    
    def get_role(self):
        return self.char_role
    
    def get_inventory(self):
        return self.inventory

    def get_stats(self):
        return self.stats
    
    def get_stat_points(self):
        return self.stat_point
    
    def get_raw_stats(self):
        return self.raw_stats
    
    def get_skills(self):
        return self.skills
    
    def get_abilities(self):
        abilities = []

        for ability in self.char_role.get_abilities():
            if ability['req_level'] <= self.char_level:
                abilities.append(ability)

        return abilities
    
    def get_modifier(self, stat_name: str):
        if stat_name in self.STATS:
            # Modifier = (Ability Score - 10) / 2 (rounded down)
            return round((self.stats[stat_name] - 10) / 2)

    def get_combat_ready(self):
        return self.combat_ready
    
    def get_weapon(self):
        return self.inventory.get_items()['equipment']['main_weapon']
    
    def get_combat_claims(self):
        return self.combat_claims
    
    def get_items(self):
        return self.inventory.get_items()
    
    # =========================================================
    # SETS
    # =========================================================
    def set_ent_type(self, ent_type):
        self.ent_type = ent_type

    def set_entity_id(self, entity_id):
        if type(entity_id) is not str:
            entity_id = str(entity_id)

        if self.ent_type == 'Character':
            if not entity_id.startswith('@'):
                entity_id = '@' + entity_id

        self.entity_id = entity_id
    
    def set_raw_stats(self, raw_stats):
        self.raw_stats = raw_stats

    def set_stat(self, stat_value: int, character_stat: str):
        if stat_value <= self.stat_point and character_stat in self.STATS:
            self.stats[character_stat] += stat_value
            self.stat_point -= stat_value

    def set_raw_stat(self, raw_stat_index: int, character_stat: str, empty: bool):
        if empty:
            self.raw_stats = []

        else:
            self.raw_stats.sort(reverse=True)

            if 0 <= raw_stat_index < len(self.raw_stats):
                if character_stat in self.STATS:
                    self.stats[character_stat] = self.raw_stats[raw_stat_index]
    
    def set_level(self, level: int):
        self.char_level = level

    def set_exp(self, exp: int):
        self.cur_exp += exp

    def set_req_exp(self, exp: int):
        self.req_exp = exp
    
    def set_role(self, role: str):
        """
        Set the character's role (class)
        
        :param role: The role to assign to the character
        :type role: str
        """
        try:
            self.char_role = Role(role)
            self.description = f"You are {self.name} a {self.gender} {self.race} {self.char_role.role_name}"

        except Exception as e:
            return "Role assign failed " + str(e)
        
        return True

    def set_value(self, key, value):
        if key == "inventory":
            new_inventory = Inventory()
            new_inventory.port(value)
            self.inventory = new_inventory

        else:
            setattr(self, key, value)
        
        print(f"Set Character {key} to {value}")

    def set_default_equip(self, equip_type):
        equipment = self.inventory.items['equipment']
        equip = {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}}

        if equip_type in equipment.keys():
            equip = ""

            if equip_type == 'main_weapon':
                equip = {"id": 7, "name": "Bare hands", "item_type": "weapon", "description": "", "attack_type": "melee", "dice_roll": "1d4", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}}
            else:
                equip = {"id": 0, "name": "Empty", "item_type": "equip", "description": "", "attack_type": "", "dice_roll": "", "base_drop_rate": 0, "base_drop_rate": 0, "base_drop_rate": 0, "effects": {}}

            self.inventory.items['equipment'][equip_type] = equip

        return equip