# This class handles all they different type of encounters (explorations, battles, etc.)

class Encounter:

    # =========================================================
    # INIT
    # =========================================================
    def __init__(self):
        self.encounter_type = ""
        self.friendly = []
        self.enemies = []
        pass
    

    # =========================================================
    # Main methods
    # =========================================================
    def create(self, encounter_type = "Battle", friendly = None, enemies = None):
        # Starts a new encounter
        self.encounter_type = encounter_type

        if friendly is not None:
            self.add_friendly(friendly)

        if enemies is not None:
            self.add_enemies(enemies)


    def add_partecipants(self, friendly, enemies):
        self.friendly = friendly
        self.enemies = enemies

    def add_friendly(self, friendly):
        self.friendly = friendly

    def add_enemies(self, enemies):
        self.enemies = enemies

    def finish(self):
        # Process results and drops
        pass
    
    
    
    # =========================================================
    # Gets
    # =========================================================
    def get_friendly(self):
        return self.friendly
    
    def get_enemies(self):
        return self.enemies