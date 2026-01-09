# Main Warrior class file

class Warrior:
    ABILITY_TREE = {
        "Slash": {
            "description": "You swing your {main_weapon} in the most basic of ways.",
            "usage_lines": {
                "cast": "swings {pronoun_self} {main_weapon} against {target_name}...",
                "success": "The swing connects and does {dmg} {dmg_type} damage to {target_name}!",
                "fail": "The swing goes wide..."
            },
            "reqs": {
                "level": 1,
                "hp": 0,
                "mp": 0,
                "sp": 10,
            },
            "effects": {}
        },
        "Split Slash": {
            "description": "A powerful vertical move that has a chance to stagger the enemy.",
            "usage_lines": {
                "cast": "You slash your {main_weapon} against your target!",
                "success": "Your slash connects and does {dmg} {dmg_type} to your enemy.",
                "fail": "The slash goes wide..."
            },
            "reqs": {
                "level": 10,
                "hp": 0,
                "mp": 0,
                "sp": 20,
            },
            "effects": {
                "stagger": 0.15
            }
        },
    }

    ABILITY_NAMES = ["Slash", "Split Slash"]
    HP_MODIFIER = 1.10
    MP_MODIFIER = 0.80
    SP_MODIFIER = 1.05
    MAIN_RESOURCE = "sp"
    MAIN_STAT = "strength"
    SUB_STAT = "constitution"
    


