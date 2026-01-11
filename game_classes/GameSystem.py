import os, base64, json, pickle, sqlite3
from .Character import Character

class GameSystem:
    NO_RP_CHARACTER_ERROR = "You don't have a RP character currently."
    NO_DB_DATA_ERROR = "No data found"
    NO_CHARACTER_FOUND_ERROR = "Character not found or not loaded"
    
    db_connection = ""
    db_cursor = ""

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        self.db_connection = sqlite3.connect('./game_db/main.db')
        self.db_connection.row_factory = lambda cursor, row: {col[0] : row[i] for i,col in enumerate(cursor.description)}
        self.db_cursor = self.db_connection.cursor()

    

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
        query_res = self.db_cursor.execute(query)

        if query_res.fetchone() is None:
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
            query_res = self.db_cursor.execute(query)

            character = Character()
            character.load(query_res.fetchall()[0])

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
            print(f"Saving character {user_id}...")
            # Search for the character in the db
            query = "SELECT id from Entities WHERE uid = " + str(user_id)
            query_res = self.db_cursor.execute(query)

            if query_res.fetchone() is None:
                # No char found in DB, Insert
                query = ("INSERT INTO `Entities` "
                            "(uid, ent_type, name, surname, gender, race, height, weight, nsfw, description, backstory, char_role, char_level, role_level, mhp, mmp, msp, hp, mp, sp, ac, cur_exp, req_exp, raw_stats, stat_point, stats, skills, abilities, inventory) "
                            "VALUES(:uid, :ent_type, :name, :surname, :gender, :race, :height, :weight, :nsfw, :description, :backstory, :char_role, :char_level, :role_level, :mhp, :mmp, :msp, :hp, :mp, :sp, :ac, :cur_exp, :req_exp, :raw_stats, :stat_point, :stats, :skills, :abilities, :inventory);")

            else:
                # Char exists, Update
                query = ("UPDATE `Entities` SET "
                            "name = :name, surname = :surname, gender = :gender, race = :race, "
                            "height = :height, weight = :weight, nsfw = :nsfw, description = :description, backstory = :backstory, "
                            "char_role = :char_role, char_level = :char_level, role_level = :role_level, "
                            "mhp = :mhp, mmp = :mmp, msp = :msp, hp = :hp, mp = :mp, sp = :sp, ac = :ac, "
                            "cur_exp = :cur_exp, req_exp = :req_exp, "
                            "raw_stats = :raw_stats, stat_point = :stat_point, stats = :stats, "
                            "skills = :skills, abilities = :abilities, inventory = :inventory "
                            "WHERE uid = :uid;")
                
            data = vars(character)
            data["uid"] = user_id
            data['char_role'] = character.get_role().role_name
            data['raw_stats'] = json.dumps(character.get_raw_stats())
            data['stats'] = json.dumps(character.get_stats())
            data['skills'] = json.dumps(character.get_skills())
            data['abilities'] = json.dumps(character.get_abilities())
            data['inventory'] = json.dumps(vars(character.get_inventory()))
            print(data)

            self.db_cursor.execute(query, data)
            self.db_connection.commit()

    def delete_character(self, user_id: int):
        # Search for the character in the db
        query = "SELECT id from Entities WHERE uid = " + str(user_id)
        query_res = self.db_cursor.execute(query)

        if query_res.fetchone() is None:
            # No char in DB
            # try remove char file
            try:
                os.remove('./game_saves/character_'+str(user_id)+'.pickle')

            except Exception:
                print(f"Character file with uid: {user_id} not found in fs.")

        else:
            query_del = ("DELETE FROM `Entities` "
                         "WHERE uid = :uid;")
            data = {
                "uid": user_id
            }

            self.db_cursor.execute(query_del, data)
            self.db_connection.commit()