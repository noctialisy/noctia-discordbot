import os, base64, json, pickle, mariadb
from .Character import Character

class GameSystem:
    NO_RP_CHARACTER_ERROR = "You don't have a RP character currently."
    NO_DB_DATA_ERROR = "No data found"
    NO_CHARACTER_FOUND_ERROR = "Character not found or not loaded"
    
    db_connection = ""
    db_cursor = ""
    settings = []

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self, db_name=None):
        if db_name is None:
            db_name = 'game_example'

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

    
    # =========================================================
    # Discord Section
    # =========================================================
    def get_discord_characters(self, uid = None):
        query = "SELECT * FROM Entities;"
        query_res = self.db_cursor.execute(query)

        if query_res.fetchone() is None:
            return self.NO_DB_DATA_ERROR
        
        else:
            # Return the ability
            result = query_res.fetchall()

            if uid is None:
                return result
            else:
                return map(lambda row: row[uid] == uid, result)
    
    

    # =========================================================
    # Character Section
    # =========================================================
    def load_character(self, user_id: int):
        """
        Load the character from the database, can also check for existence
        
        :param user_id: Specify the user reference id for the character to load
        :type user_id: int

        :return: Character loaded if load ok, otherwise str
        :rtype: Character
        """
        character = ""

        # Search for the character in the db
        query = "SELECT id from Entities WHERE uid = " + str(user_id)
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        if result == []:
            # No char found
            # Try user file
            try:
                with open('./game_saves/character_'+str(user_id)+'.pickle', 'rb') as file:

                    # Compatibility
                    print(f"Adding file to db compatibility for {user_id}...")
                    new_character = Character()
                    old_character = pickle.load(file)
                    old_data = vars(old_character)
                    print(old_data)
                    print()

                    for key, item in old_data.items():
                        if key == "type":
                            key = "ent_type"

                        if key == "exp":
                            key = "cur_exp"

                        if key == "role":
                            key = "char_role"

                        if key == "level":
                            key = "char_level"

                        if key == "role_name":
                            new_character.set_role(item)
                            continue

                        new_character.set_value(key, item)

                    new_character.calc_stats()
                    print(f"New stats calculated for the char {user_id} \n")
                    self.save_character(user_id, new_character)

                    return new_character
                
            except Exception as e:
                print(f"There was an exception loading the character {user_id} from file: ")
                print(e)
                return self.NO_CHARACTER_FOUND_ERROR
            
        else:
            query = "SELECT * from Entities WHERE uid = " + str(user_id)
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchall()


            character = Character()
            character.load(result[0])

            return character

    def save_character(self, user_id: int, character: Character, save_method = "db"):
        """
        Save the character to the database
        
        :param user_id: Specify the user reference id for the character to save
        :type user_id: int
        :param character: The character to save
        :type character: Character
        """

        if save_method == "file":
            with open('./game_saves/character_'+str(user_id)+'.pickle', 'wb') as file:
                pickle.dump(character, file)

        else:
            #print(f"Saving character {user_id}...")
            # Search for the character in the db
            query = "SELECT id from Entities WHERE uid = " + str(user_id)
            self.db_cursor.execute(query)
            query_res = self.db_cursor.fetchall()

            # Must transform the data because vars() returns a pointer to the class values
            save_data = {}
            data = vars(character)

            for key in data.keys():
                attr_value = getattr(character, key)
                save_data[key] = attr_value

            save_data["uid"] = user_id
            save_data['char_role'] = character.get_role().role_name
            save_data['raw_stats'] = json.dumps(character.get_raw_stats())
            save_data['stats'] = json.dumps(character.get_stats())
            save_data['skills'] = json.dumps(character.get_skills())
            save_data['abilities'] = json.dumps(character.get_abilities())
            save_data['inventory'] = json.dumps(vars(character.get_inventory()))

            if save_data['height'] == "":
                save_data['height'] = 0
            
            if save_data['weight'] == "":
                save_data['weight'] = 0

            if query_res == []:
                # No char found in DB, Insert
                query = ("INSERT INTO `Entities` "
                            "(uid, ent_type, name, surname, gender, race, height, weight, nsfw, description, backstory, char_role, char_level, role_level, mhp, mmp, msp, hp, mp, sp, ac, cur_exp, req_exp, raw_stats, stat_point, stats, skills, abilities, inventory) "
                            f"VALUES(\"{save_data["uid"]}\", \"{save_data["ent_type"]}\", \"{save_data["name"]}\", \"{save_data["surname"]}\", \"{save_data["gender"]}\", \"{save_data["race"]}\", {int(save_data["height"])}, {int(save_data["weight"])}, "
                            f"{int(save_data["nsfw"])}, \"{save_data["description"]}\", \"{save_data["backstory"]}\", \"{save_data["char_role"]}\", {save_data["char_level"]}, "
                            f"{save_data["role_level"]}, {save_data["mhp"]}, {save_data["mmp"]}, {save_data["msp"]}, {save_data["hp"]}, {save_data["mp"]}, {save_data["sp"]}, {save_data["ac"]}, "
                            f"{save_data["cur_exp"]}, {save_data["req_exp"]}, '{save_data["raw_stats"]}', {save_data["stat_point"]}, '{save_data["stats"]}', '{save_data["skills"]}', '{save_data["abilities"]}', '{save_data["inventory"]}');")

            else:
                # Char exists, Update
                query = (f"UPDATE `Entities` SET "
                            f"name = \"{save_data["name"]}\", surname = \"{save_data["surname"]}\", gender = \"{save_data["gender"]}\", race = \"{save_data["race"]}\", "
                            f"height = {int(save_data["height"])}, weight = {int(save_data["weight"])}, nsfw = {int(save_data["nsfw"])}, description = \"{save_data["description"]}\", backstory = \"{save_data["backstory"]}\", "
                            f"char_role = \"{save_data["char_role"]}\", char_level = {save_data["char_level"]}, role_level = {save_data["role_level"]}, "
                            f"mhp = {save_data["mhp"]}, mmp = {save_data["mmp"]}, msp = {save_data["msp"]}, hp = {save_data["hp"]}, mp = {save_data["mp"]}, sp = {save_data["sp"]}, ac = {save_data["ac"]}, "
                            f"cur_exp = {save_data["cur_exp"]}, req_exp = {save_data["req_exp"]}, "
                            f"raw_stats = '{save_data["raw_stats"]}', stat_point = {save_data["stat_point"]}, stats = '{save_data["stats"]}', "
                            f"skills = '{save_data["skills"]}', abilities = '{save_data["abilities"]}', inventory = '{save_data["inventory"]}' "
                            f"WHERE uid = \"{save_data["uid"]}\";")
            

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