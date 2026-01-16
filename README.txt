# D&D Game engine supporting Discord through a bot

This project handles the discord bot for Rose Garden ([Noctialisy](https://twitch.tv/noctialisy)'s community) and contains the code for the D&D game based on Noctialisy's lore.
The code hosted in this repo is available to view, but protected by copyright. You can view the code and study it for academical reasons.
If you want to use the bot / game for your own server, contact me.


## Requirements
  - Python 3.12
  - MariaDB


## Install / Run

  Before running the bot remember to:
    1 - Fill in the settings_example.json file
    2 - Rename settings_example.json to settings.json
    3 - Create a database (MariaDB works better) using the base query in game_db/example.sql

    If you're building for docker / kubernetes there's included a dockerfile for the image and a k8s file for docker.
    You can generate the ready files by using the command python handle.py build (Need to fill settings.json first)

    Optional - There's included a Test.py class to run some minimal game test (doesn't test the discord part for now)
    You can run a test before releasing / running the bot with python test.py (test is fully automated)
    Test requires 2 databases:
      1 with the table structure from game_db/example.sql (for checks)
      1 with test data (suggested a duplicate of your game db, if you're starting you can use your production schema)


## What you can do right now:
  - Create your RP character (supports only one per server member, can create more tho)
  - Assign your stats after the initial D&D stat rolls
  - Rest and use abilities (There's a limited number of abilities, I'm expanding on them)
  - Roll dices (base ones or using your RP character if you have one)
  - Battle each other (through the use of abilities)
  - Spawn an enemy (Only people that have the GM role) [Can spawn with stats or randomly]
  - Get exp by winning a fight


## In the future:
  - Allow people to check their skills and get a list of enemies spawned
  - Allow for enemy claiming (have a reference of the user that attacked an enemy) for drops calculations
  - Having the lore from my wiki expanded and added into the game
  - Allowing people to start threads for their RP sessions (adventures)
  - Generating stories using AI (at first until I can write down an algorithm to procedurally generate things)
  - Eventually (probably) releasing the bot to the public so people will have their D&D game engine for D&D based games that can run in discord, a browser or a standalone game app
  - Splitting the game code and the bot so that the game can be ported elsewhere

  Currently working on:
    - Database and items
    - Battle system


## Available and tested commands for now:

  - /create_character -> Create your RP character
  - /check_character -> Will give you a very basic description of your character
  - /set_character_stats_order -> Will allow you to set the character stats order for your character based on your initial rolls
  - /delete_character -> Deletes your character so you can start over. This is unreverable.

  - /rp_rest -> Make your character rest (This restores HP/MP/SP and allows you to level up)
  - /rp_action -> Allow you to cast a skill on self or a target (Base skills are Attack, Defend, Heal, Pat... etc)
  - /rp_spawn_enemy -> Spawns an Enemy either randomly or with set stats (Can only be used by GMs - People with GM role)

  - /roll_dice -> Roll one or more D&D dices (If you have an RP character those rolls take into account your stats, otherwise are generic)


## Copyright

  This work is protected by copyright. All rights are reserved