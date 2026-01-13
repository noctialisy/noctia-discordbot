# Main class for handling character roles (Mage, Warrior, Paladin, Dancer, etc.)
import json, mariadb

class Role:
    ROLES = []
    role_name = ""
    role_hit_dice = ""
    role_magic_dice = ""
    role_special_dice = ""
    role_abilities = []

    NO_DB_DATA_ERROR = "No data found"

    db_connection = ""
    db_cursor = ""

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self, role_name :str):

        with open('./settings.json', 'r', encoding='utf-8') as settings_file:
            self.settings = json.loads(settings_file.read())


        self.db_connection = mariadb.connect(
            user=self.settings['db_user'],
            password=self.settings['db_pass'],
            host=self.settings['db_host'],
            port=self.settings['db_port'],
            database=self.settings['db_name'],
            autocommit=True,

        )
        self.db_cursor = self.db_connection.cursor(dictionary=True)

        self.ROLES = self.get_role_names()

        if self.ROLES == self.NO_DB_DATA_ERROR:
            print("Role class had a db fetching error!")
            self.ROLES = []

        if role_name in self.ROLES:
            self.role_name = role_name
            self.role_hit_dice = self.get_role_hit_dice(self.role_name)
            self.role_magic_dice = self.get_role_magic_dice(self.role_name)
            self.role_special_dice = self.get_role_special_dice(self.role_name)
            self.role_abilities = self.get_role_abilities(self.role_name)
        else:
            print("Role class had a db fetching error!")
            self.role_name = "Not Init"

    
    # =========================================================
    # Main methods
    # =========================================================
    def use_ability(self, entity, mp, sp, ability_name, trg_entity):
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
        
        # Use ability
        ability_lines = {
            "cast": ability['usage_line_cast'],
            "success": ability['usage_line_success'],
            "fail": ability['usage_line_fail']
        }

        for key, value in ability_lines.items():
            ability_lines[key] = str(ability_lines[key]).replace('{entity_name}', entity.name)
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
            #ability_lines = self.role_class.ABILITY_TREE[ability_name]['usage_lines']

            for key, value in ability_lines.items():
                ability_lines[key] = str(ability_lines[key]).replace('{dmg}', str(dmg))
                ability_lines[key] = str(ability_lines[key]).replace('{dmg_type}', str('physical'))

            return ["success", ability_lines]
        
        else:
            return ["fail", ability_lines]

    def calculate_dmg(self, entity, trg_entity):
        dmg = entity.roll_dice("d10")
        return dmg
    

    
    # =========================================================
    # Gets
    # =========================================================
    def get_role_names(self):
        query = "SELECT name FROM Roles;"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            # Return the roles
            data = map(lambda row: row['name'], result)
            return list(data)

    def get_role_hit_dice(self, role_name):
        query = f"SELECT hit_dice FROM Roles WHERE name = \"{role_name}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            data = map(lambda row: row['hit_dice'], result)
            return list(data)[0]
        
    def get_role_magic_dice(self, role_name):
        query = f"SELECT magic_dice FROM Roles WHERE name = \"{role_name}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            data = map(lambda row: row['magic_dice'], result)
            return list(data)[0]
        
    def get_role_special_dice(self, role_name):
        query = f"SELECT special_dice FROM Roles WHERE name = \"{role_name}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            data = map(lambda row: row['special_dice'], result)
            return list(data)[0]
    
    def get_role_abilities(self, role_name):
        any_role = "Any"
        query = f"SELECT * FROM Abilities WHERE role_name = \"{role_name}\" OR role_name = \"{any_role}\";"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            return self.NO_DB_DATA_ERROR
        
        else:
            # Return the ability list
            return result