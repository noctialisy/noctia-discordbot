# Main entity class, it is the base for NPCs, Enemies and Characters
import os, json, pickle

from .GameSystem import GameSystem
from .Role import Role
from .Inventory import Inventory
from .Dice import Dice

class Entity(GameSystem):
    RACES = ["Human", "Elf", "Catfolk", "Kitsune", "Lupine", "Orc"]
    GENDERS = ["Male", "Female"]
    STATS = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    ROLES = ["Any", "Warrior", "Mage"]
    MAX_LEVEL = 10

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
        self.abilities = []

        self.inventory = Inventory()
    
    
    
    # =========================================================
    # MAINS
    # =========================================================
    def load(self, vars):
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
        self.abilities = json.loads(vars['abilities'])
        self.inventory = Inventory(json.loads(vars['inventory']))
    
    def load_character(self, entity, user_id: int):
        """
        Load the character from the database, can also check for existence
        
        :param user_id: Specify the user reference id for the character to load
        :type user_id: int

        :return: Character loaded if load ok, otherwise str
        :rtype: Character
        """

        # Search for the character in the db
        query = f"SELECT id from Entities WHERE uid = '{str(user_id)}';"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            # No char found
            # Try user file
            return self.NO_CHARACTER_FOUND_ERROR
            
        else:
            query = f"SELECT * from Entities WHERE uid = '{str(user_id)}';"
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchall()

            entity.load(result[0])

            return entity

    def save_character(self, user_id: int, save_method = "db"):
        """
        Save the character to the database
        
        :param user_id: Specify the user reference id for the character to save
        :type user_id: int
        :param character: The character to save
        :type character: Character
        """

        if save_method == "file":
            with open('./game_saves/character_'+str(user_id)+'.pickle', 'wb') as file:
                pickle.dump(self, file)

        else:
            #print(f"Saving character {user_id}...")
            # Search for the character in the db
            query = "SELECT id from Entities WHERE uid = " + str(user_id)
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

            if save_data['height'] == "":
                save_data['height'] = 0
            
            if save_data['weight'] == "":
                save_data['weight'] = 0

            if query_res == []:
                # No char found in DB, Insert
                query = ("INSERT INTO `Entities` "
                            "(uid, ent_type, name, surname, gender, race, height, weight, nsfw, description, backstory, char_role, char_level, role_level, mhp, mmp, msp, hp, mp, sp, ac, cur_exp, req_exp, raw_stats, stat_point, stats, skills, abilities, inventory) "
                            f"VALUES(\"{save_data['uid']}\", \"{save_data['ent_type']}\", \"{save_data['name']}\", \"{save_data['surname']}\", \"{save_data['gender']}\", \"{save_data['race']}\", {int(save_data['height'])}, {int(save_data['weight'])}, "
                            f"{int(save_data['nsfw'])}, \"{save_data['description']}\", \"{save_data['backstory']}\", \"{save_data['char_role']}\", {save_data['char_level']}, "
                            f"{save_data['role_level']}, {save_data['mhp']}, {save_data['mmp']}, {save_data['msp']}, {save_data['hp']}, {save_data['mp']}, {save_data['sp']}, {save_data['ac']}, "
                            f"{save_data['cur_exp']}, {save_data['req_exp']}, '{save_data['raw_stats']}', {save_data['stat_point']}, '{save_data['stats']}', '{save_data['skills']}', '{save_data['abilities']}', '{save_data['inventory']}');")

            else:
                # Char exists, Update
                query = (f"UPDATE `Entities` SET "
                            f"name = \"{save_data['name']}\", surname = \"{save_data['surname']}\", gender = \"{save_data['gender']}\", race = \"{save_data['race']}\", "
                            f"height = {int(save_data['height'])}, weight = {int(save_data['weight'])}, nsfw = {int(save_data['nsfw'])}, description = \"{save_data['description']}\", backstory = \"{save_data['backstory']}\", "
                            f"char_role = \"{save_data['char_role']}\", char_level = {save_data['char_level']}, role_level = {save_data['role_level']}, "
                            f"mhp = {save_data['mhp']}, mmp = {save_data['mmp']}, msp = {save_data['msp']}, hp = {save_data['hp']}, mp = {save_data['mp']}, sp = {save_data['sp']}, ac = {save_data['ac']}, "
                            f"cur_exp = {save_data['cur_exp']}, req_exp = {save_data['req_exp']}, "
                            f"raw_stats = '{save_data['raw_stats']}', stat_point = {save_data['stat_point']}, stats = '{save_data['stats']}', "
                            f"skills = '{save_data['skills']}', abilities = '{save_data['abilities']}', inventory = '{save_data['inventory']}' "
                            f"WHERE uid = \"{save_data['uid']}\";")
            

            self.db_cursor.execute(query)

    def delete_character(self, user_id: int):
        # Search for the character in the db
        query = "SELECT id from Entities WHERE uid = " + str(user_id)
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            # No char in DB
            # try remove char file
            try:
                os.remove('./game_saves/character_'+str(user_id)+'.pickle')

            except Exception:
                print(f"Character file with uid: {user_id} not found in fs.")

        else:
            query_del = ("DELETE FROM `Entities` "
                         f"WHERE uid = \"{user_id}\";")

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
    
    def use_ability(self, ability_name, targets=[]):
        if type(targets) is not list:
            if targets is not None:
                targets = [targets]

            else:
                targets = []

        return self.char_role.use_ability(self, self.mp, self.sp, ability_name, targets)    

    def check_level_up(self):
        if self.cur_exp >= self.req_exp and self.cur_exp != 0:
            if self.char_level < self.MAX_LEVEL:
                self.level_up()

    def level_up(self):
        self.cur_exp -= self.req_exp

        if self.cur_exp < 0:
            self.cur_exp = 0

        self.char_level += 1
        self.req_exp += (self.req_exp * 2)
        self.stat_point += 1
        self.calc_stats()

    def calc_stats(self):
        if type(self.char_role) == str:
            self.char_role = Role(self.char_role)
        
        # Get specific dices for the Role
        hit_dice = self.char_role.role_hit_dice
        magic_dice = self.char_role.role_magic_dice
        special_dice = self.char_role.role_special_dice

        if self.char_level == 1:
            # At start, Max dice + modifier
            self.mhp = int(hit_dice.split("d")[1]) + self.get_modifier('constitution')
            self.mmp = int(magic_dice.split("d")[1]) + self.get_modifier('intelligence')
            self.msp = int(special_dice.split("d")[1]) + self.get_modifier('dexterity')

        else:
            # Lv2+, dice_roll + modifier
            self.mhp += self.roll_dice(hit_dice)[0] + self.get_modifier('constitution')
            self.mmp += self.roll_dice(magic_dice)[0] + self.get_modifier('intelligence')
            self.msp += self.roll_dice(special_dice)[0] + self.get_modifier('dexterity')

    def rest(self):
        self.check_level_up()
        self.hp = self.mhp
        self.mp = self.mmp
        self.sp = self.msp
    
    def apply_dmg(self, dmg_amt):
        if self.hp >= dmg_amt:
            self.hp = self.hp - dmg_amt
        else:
            self.hp = 0

        self.save_character(self, self.entity_id)

    def apply_heal(self, heal_amt):
        total_hp_after_heal = self.hp + heal_amt

        if total_hp_after_heal > self.mhp:
            self.hp = self.mhp
        else:
            self.hp = total_hp_after_heal

        self.save_character(self, self.entity_id) 
    
    def drop_items(self):
        # Add drops mechanics
        pass
    
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


    # =========================================================
    # GETS
    # =========================================================
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
        return self.abilities
    
    def get_modifier(self, stat_name: str):
        if stat_name in self.STATS:
            # Modifier = (Ability Score - 10) / 2 (rounded down
            return round((self.stats[stat_name] - 10) / 2)



    # =========================================================
    # SETS
    # =========================================================
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
        self.cur_exp = exp

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