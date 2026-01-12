# ===============================================
# Import
# ===============================================
# Main imports
# -------------------------------------
import os, shutil, pathlib, json, random, discord
import traceback
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


    # ===============================================
    # Init
    # ===============================================
    def __init__(self):
        try:
            example_db_file = Path('./game_db/example.db')
            test_db_file = Path('./game_db/test.db')

            if example_db_file.is_file():
                
                # Failed before or other cases (Clean)
                if test_db_file.is_file():
                    os.remove(test_db_file)

                shutil.copy2(example_db_file, test_db_file)
                self.game_system = GameSystem(test_db_file)

            else:
                raise Exception('## Example DB missing. Can\'t run')
            

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
            query = "SELECT sql from sqlite_schema WHERE name = :name"
            data = {"name": table}

            try:
                self.game_system.db_cursor.execute(query, data)
                test = self.game_system.db_cursor.fetchall()

                if test is None:
                    raise Exception('Table not found!')
                
                with open('./game_db/sql/' + str(table).lower() + '.sql', 'r', encoding='utf-8') as schema_file:
                    table_supposed_schema = schema_file.read()

                    # Create the test table
                    create_query = table_supposed_schema.replace("CREATE TABLE "+str(table), "CREATE TABLE "+str(table)+"2")
                    self.game_system.db_cursor.execute(create_query)

                    # Find the test table
                    query = "SELECT sql from sqlite_schema WHERE name = :name"
                    data = {"name": str(table)+"2"}
                    self.game_system.db_cursor.execute(query, data)
                    test_table = self.game_system.db_cursor.fetchall()
                    test_table = test_table[0]['sql']
                    test_schema = str(test_table).replace("CREATE TABLE "+str(table)+"2", "CREATE TABLE "+str(table))

                    # Check if the schema matches
                    if table_supposed_schema != test_schema:
                        print(table_supposed_schema)
                        print()
                        print(test_schema)
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
                print("## Rolled stats: ")
                print(results)
            
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
    
    # Close db connections
    async def close_db_connection(self):
        self.game_system.db_cursor.close()
        self.game_system.db_connection.close()

    # Clean the test
    async def clean_test(self):
        await self.close_db_connection()
        os.remove('./game_db/test.db')
        print('## Tests completed.')

