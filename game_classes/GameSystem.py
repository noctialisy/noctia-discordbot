import os, pickle
from .Character import Character

class GameSystem:

    def load_character(user_id: int):
        """
        Load the character from the database, can also check for existence
        
        :param user_id: Specify the user reference id for the character to load
        :type user_id: int

        :return: Character loaded if load ok, otherwise str
        :rtype: Character
        """
        character = ""

        try:
            with open('./game_saves/character_'+str(user_id)+'.pickle', 'rb') as file:
                character = pickle.load(file)
                return character
            
        except Exception:
            return "Character not found or not loaded"
        

    def save_character(user_id: int, character: Character):
        """
        Save the character to the database
        
        :param user_id: Specify the user reference id for the character to save
        :type user_id: int
        :param character: The character to save
        :type character: Character
        """
        with open('./game_saves/character_'+str(user_id)+'.pickle', 'wb') as file:
            pickle.dump(character, file)

    def delete_character(user_id: int):
        os.remove('./game_saves/character_'+str(user_id)+'.pickle')