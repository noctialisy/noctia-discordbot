# ===============================================
# Import
# ===============================================
# Main imports
# -------------------------------------
import os, shutil, pathlib, json, random, discord
import mariadb, traceback
from pathlib import Path
from discord.ext import commands
from discord.commands import option


# Game imports
# -------------------------------------
from .GameSystem import GameSystem
from .Character import Character
from .Enemy import Enemy
from .Dice import Dice


class Test:
    game_system = ""
    conn_example = ""
    cur_example = ""
    conn_test = ""
    cur_test = ""
    settings = []


    # ===============================================
    # Init
    # ===============================================
    def __init__(self):
        self.game_system = GameSystem('game_test')
        
        try:
            with open('./settings.json', 'r', encoding='utf-8') as settings_file:
                self.settings = json.loads(settings_file.read())

            example_db = "game_example"
            test_db = "game_test"

            self.conn_example = mariadb.connect(
                user=self.settings['db_user'],
                password=self.settings['db_pass'],
                host=self.settings['db_host'],
                port=self.settings['db_port'],
                database=example_db,
                autocommit=True,

            )
            self.cur_example = self.conn_example.cursor(dictionary=True)

            self.conn_test = mariadb.connect(
                user=self.settings['db_user'],
                password=self.settings['db_pass'],
                host=self.settings['db_host'],
                port=self.settings['db_port'],
                database=test_db,
                autocommit=True,

            )
            self.cur_test = self.conn_test.cursor(dictionary=True)

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return

        except Exception as e:
            print("## Can't initialize GameSystem class on test.db")
            print(e)
            return

    
    
    # ===============================================
    # Main methods
    # ===============================================
    # Test database tables
    def test_db(self):
        print('## DB test start ===')
        tables = ["Abilities", "Entities", "Roles"]

        for table in tables:
            query = "DESCRIBE " + table

            try:
                self.cur_example.execute(query)
                example_table = self.cur_example.fetchall()

                self.cur_test.execute(query)
                test_table = self.cur_test.fetchall()

                # Check if the schema matches
                if test_table != example_table:
                    print(example_table)
                    print()
                    print(test_table)
                    raise Exception(f'## The table {table} is malformed for this version.')
                    
            except Exception as e:
                print(f'## There was a problem with the table {table}')
                print(traceback.format_exc())
                print(e)
                return

        print('## DB test pass!')

    # Test the character class
    def test_character(self, uid=50, name='Test', surname='Test', race='Human', gender='Female', role='Mage', nsfw=True):
        print('## Character test start ===')
        try:
            # Create Character
            character = Character()
            creation_result = character.create(name, surname, race, gender, nsfw)

            if 'Creating failed' in creation_result:
                raise Exception('## Character creation failed! ' + str(creation_result))
            
            # Assign role
            set_role_result = character.set_role(role)

            if type(set_role_result) is str:
                raise Exception('## Character role assignation failed! ' + str(set_role_result))
            
            # Roll stats
            results = character.roll_stats()

            if type(results) is not list:
                raise Exception('## Character can\'t roll stats')
            else:
                print("## Rolled stats: "+ str(results))
            
            # Assign stats
            character.set_raw_stat(0, "strength", False)
            character.set_raw_stat(1, "constitution", False)
            character.set_raw_stat(2, "dexterity", False)
            character.set_raw_stat(3, "intelligence", False)
            character.set_raw_stat(4, "wisdom", False)
            character.set_raw_stat(5, "charisma", False)
            character.set_raw_stat(0, "", True)

            # Calculate
            character.calc_stats()

            # Save Character
            # It is critical to move the values out of vars() because of pointers
            character_data = vars(character)
            saved_char_data = {}
            for key in character_data.keys():
                value = getattr(character, key)
                saved_char_data[key] = value


            self.game_system.save_character(uid, character)

            # Load Character
            new_character = self.game_system.load_character(uid)
            character_data = vars(new_character)
            loaded_char_data = {}
            for key in character_data.keys():
                value = getattr(new_character, key)
                loaded_char_data[key] = value
            
            # Normalize load data to save data
            # This is necessary because object instances will always differ and will create false positives
            loaded_char_data['nsfw'] = bool(loaded_char_data['char_role'])
            
            saved_char_data['char_role'] = saved_char_data['char_role'].role_name
            loaded_char_data['char_role'] = loaded_char_data['char_role'].role_name

            saved_char_data['inventory'] = saved_char_data['inventory'].print()
            loaded_char_data['inventory'] = loaded_char_data['inventory'].print()


            if saved_char_data != loaded_char_data:
                print('\n')
                print('Saved Data: \n')
                print(saved_char_data)

                print('\n')
                print('Loaded Data: \n')
                print(loaded_char_data)
                raise Exception('## Character Save and Load data differ')

            # Rest
            character.rest()

            # Use ability
            ability_use_result = character.use_ability('Attack', new_character)

            # Describe character
            print('## Describe yourself...')
            description = character.describe()
            print(description)

            if ability_use_result == "No abilities":
                raise Exception('## The character doesn\'t has that ability')
            else:
                print("## Ability cast result: " + str(ability_use_result))
            
            # Check user search
            self.game_system.get_discord_characters(uid)

            # Delete character
            self.game_system.delete_character(uid)

        
        except Exception as e:
            print('## Character class failed some tests.')
            print(e)
            print(traceback.format_exc())
            return
        
        print('## Character test pass!')

    # Test the enemy class
    def test_enemy(self, name='Test', race=None, gender=None, role=None, nsfw=None):
        print('## Enemy test start ===')
        try:
            # Create a general enemy
            enemy = Enemy()
            creation_result = enemy.create(name,race=race,gender=gender,role=role,nsfw=nsfw)

            if type(creation_result) is str:
                raise Exception('## Enemy creation failed! ' + str(creation_result))
            
            print('## Describe yourself...')
            enemy.rest()
            description = enemy.describe()
            print(description)

        except Exception as e:
            print('## Enemy class failed some tests ')
            print(traceback.format_exc())
            print(e)
            return
        
        print('## Enemy test pass!')

    # Clean the test
    def clean_test(self):
        print('## Tests completed.')

