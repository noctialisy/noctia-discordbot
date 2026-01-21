# This class handles all they different type of encounters (explorations, battles, etc.)
import json, time


from .GameSystem import GameSystem
from .Entity import Entity


class Encounter(GameSystem):

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        super().__init__()
        self.encounter_id = 1
        self.encounter_type = ""
        self.friendly_party = []
        self.enemy_party = []
        self.locked = 0
        pass
    

    # =========================================================
    # Main methods
    # =========================================================
    # Handles system
    def create(self, encounter_type = "Battle", friendly = None, enemies = None):
        # Starts a new encounter
        self.encounter_type = encounter_type

        # Select an id for this encounter
        query = "SELECT DISTINCT encounter_id FROM Encounters ORDER BY encounter_id DESC"
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()

        self.encounter_id = 1

        if len(result) >= 1:
            self.encounter_id = int(result[0]['encounter_id']) + 1


        if type(friendly) is str:
            party_members = friendly.replace(' ', '').split(',')

            for member_id in party_members:
                entity = Entity()
                entity.ent_type = 'Character'
                result = entity.load(member_id)

                if type(result) is str:
                    print(result)
                
                if entity.encounter_id == 0:
                    entity.encounter_id = self.encounter_id

                entity.save()
                self.add_friendly(entity.entity_id)


        else:
            return "Party members not well formatted."
        
        
        if type(enemies) is str:
            enemy_members = enemies.replace(' ', '').split(',')

            for member_id in enemy_members:
                entity = Entity()
                entity.ent_type = 'Enemy'
                entity.load(member_id)
                
                if entity.encounter_id == 0:
                    entity.encounter_id = self.encounter_id

                entity.save()
                self.add_enemies(entity.entity_id)
            
        else:
            return "Enemy members not well format"
        
        
        self.start_turn()
        self.save()
        
    def save(self):
        query_check = f"SELECT encounter_id FROM Encounters WHERE encounter_id = {self.encounter_id}"
        self.db_cursor.execute(query_check)
        result = self.db_cursor.fetchall()

        data = {
            "id": self.encounter_id,
            "type": self.encounter_type,
            "friendly": json.dumps(self.friendly_party),
            "enemies": json.dumps(self.enemy_party),
            "locked": self.locked

        }

        if len(result) >= 1:
            query = f"UPDATE Encounters SET encounter_id = {data['id']}, encoutner_type = '{data['type']}', friendly_party = '{data['friendly']}', enemy_party = '{data['enemies']}', locked = {data['locked']} WHERE encounter_id = {data['id']}"

        else:
            query = f"INSERT INTO Encounters (encounter_id, encounter_type, friendly_party, enemy_party, locked) VALUES ({data['id']}, '{data['type']}', '{data['friendly']}', '{data['enemies']}', {data['locked']})"

        self.db_cursor.execute(query)

    def load(self, encounter_id):
        query_check = f"SELECT * FROM Encounters WHERE encounter_id = {encounter_id}"
        self.db_cursor.execute(query_check)
        result = self.db_cursor.fetchall()

        if len(result) >= 1:
            self.encounter_id = result[0]['encounter_id']
            self.encounter_type = result[0]['encounter_type']
            self.friendly_party = json.loads(result[0]['friendly_party'])
            self.enemy_party = json.loads(result[0]['enemy_party'])
            self.locked = result[0]['locked']

    def delete(self):
        query = f'DELETE FROM Encounters WHERE encounter_id = {self.encounter_id}'
        self.db_cursor.execute(query)
    
    def start(self):
        # Starts the encounter
        pass
    
    def finish(self):
        # Ends the encounter
        for member_id in self.friendly_party:
            entity = Entity()
            entity.ent_type = 'Character'
            result = entity.load(member_id)

            if type(result) is str:
                print(result)
            
            if entity.encounter_id != 0:
                entity.encounter_id = 0

            entity.save()
            self.add_friendly(entity.entity_id)

        

    # check if this turn can end
    def check_end_turn(self):
        can_end = True

        for member_id in self.friendly_party:
            entity = Entity()
            entity.ent_type = 'Character'
            entity.load(member_id)

            if entity.turn_ready == 0:
                continue
            else:
                can_end = False
                break


        return can_end
    
    def start_turn(self):
        for member_id in self.friendly_party:
            entity = Entity()
            entity.ent_type = 'Character'
            entity.load(member_id)
            entity.turn_ready = 1
            entity.save()
    
    # Handles Partecipants
    def add_partecipants(self, friendly, enemies):
        self.add_friendly(friendly)
        self.add_enemies(enemies)

    def add_friendly(self, friendly):
        # Check if it is a list
        if type(friendly) is not list:
            friendly = [friendly]

        for id in friendly:
            self.friendly_party.append(id)

    def add_enemies(self, enemies):
        # Check if it is a list
        if type(enemies) is not list:
            enemies = [enemies]

        for id in enemies:
            self.enemy_party.append(id)
    
    
    # =========================================================
    # Gets
    # =========================================================
    def get_friendly(self):
        return self.friendly_party
    
    def get_enemies(self):
        return self.enemy_party