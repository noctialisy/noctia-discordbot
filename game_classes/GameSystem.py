import os, json, pickle, mariadb

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
    def get_entities(self, ent_type = 'Character', uid = None):
        if type(ent_type) is not str or ent_type not in ['Character', 'Enemy']:
             ent_type = 'Character'

        query = f"SELECT * FROM Entities WHERE ent_type = '{ent_type}';"

        if type(uid) is str:
                query = f"SELECT * FROM Entities WHERE ent_type = '{ent_type}' AND uid = '{uid}';"

        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        return result