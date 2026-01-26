import os, json, pickle, mariadb

class GameSystem:
    NO_RP_CHARACTER_ERROR = "You don't have a RP character currently."
    NO_DB_DATA_ERROR = "No data found"
    NO_CHARACTER_FOUND_ERROR = "Character not found or not loaded"
    
    db_connection = ""
    db_cursor = ""
    settings = {}

    GENDERS = ["Male", "Female"]
    STATS = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    RACES = []
    ROLES = []
    MAX_LEVEL = 10

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self, db_name=None):
        if db_name is None:
            db_name = 'game_example'

        if os.path.exists('./settings.json'):
            with open('./settings.json', 'r', encoding='utf-8') as settings_file:
                self.settings = json.loads(settings_file.read())

        else:
            self.settings = {
                "discord.bot.token": os.getenv("DISCORD_BOT_TOKEN", ""),
                "discord.test.guild.id": int(os.getenv("DISCORD_TEST_GUILD", 0)),
                "discord.main.guild.id": int(os.getenv("DISCORD_MAIN_GUILD", 0)),

                "db_user": os.getenv('DB_USER', "root"),
                "db_pass": os.getenv('DB_PASS', "root"),
                "db_host": os.getenv('DB_HOST', "127.0.0.1"),
                "db_port": int(os.getenv('DB_PORT', "3306")),
                "db_name": os.getenv('DB_NAME', "game_example"),

                "debug": os.getenv('APP_DEBUG', "false")
            }

        if self.settings['app_debug'] == 'true':
            print(self.settings)

        self.db_connection = mariadb.connect(
            user=self.settings['db_user'],
            password=self.settings['db_pass'],
            host=self.settings['db_host'],
            port=self.settings['db_port'],
            database=self.settings['db_name'],
            autocommit=True,

        )
        self.db_cursor = self.db_connection.cursor(dictionary=True)
        self.RACES = self.get_db_races()
        self.ROLES = self.get_db_roles()

    
    # =========================================================
    # Discord Section
    # =========================================================
    def get_entities(self, ent_type = None, uid = None):
        query = "SELECT * FROM Entities;"

        # Select cases
        if type(ent_type) is str and type(uid) is str:
            query = f"SELECT * FROM Entities WHERE ent_type = '{ent_type}' AND uid = '{uid}';"

        elif type(ent_type) is str:
            query = f"SELECT * FROM Entities WHERE ent_type = '{ent_type}';"
        
        elif type(uid) is str:
            query = f"SELECT * FROM Entities WHERE uid = '{uid}';"
        

        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        return result
    
    def get_db_roles(self):
        query = 'SELECT DISTINCT name FROM Roles;'
        self.db_cursor.execute(query)
        tmp_results = self.db_cursor.fetchall()

        results = []

        for tmp in tmp_results:
            results.append(tmp['name'])

        return results
    
    def get_db_races(self):
        query = 'SELECT DISTINCT name FROM Races;'
        self.db_cursor.execute(query)
        tmp_results = self.db_cursor.fetchall()

        results = []

        for tmp in tmp_results:
            results.append(tmp['name'])

        return results

