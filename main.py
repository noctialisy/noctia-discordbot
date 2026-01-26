# Main imports
# -------------------------------------
import os, json, random, discord
from discord.commands import option


# Game imports
# -------------------------------------
from game_classes.Enemy import Enemy
from game_classes.Character import Character
from game_classes.Encounter import Encounter
from game_classes.Dice import Dice

# Main variables and bot intents
# -------------------------------------
discord_test_guild_id = 0
discord_main_guild_id = 0
token = ""
intents = discord.Intents.all()


# Check settings file exists
if os.path.exists('./settings.json'):
    # Settings file overwrite env
    with open('./settings.json', 'r', encoding='utf-8') as settings_file:
        
        settings = json.load(settings_file) # Load settings file, if this fails the bot won't start
        discord_test_guild_id = settings["discord.test.guild.id"]
        discord_main_guild_id = settings["discord.main.guild.id"]
        token = settings["discord.bot.token"]
        bot = discord.Bot(intents=intents)

else:
    discord_test_guild_id = int(os.getenv("DISCORD_TEST_GUILD", 0))
    discord_main_guild_id = int(os.getenv("DISCORD_MAIN_GUILD", 0))
    token = os.getenv("DISCORD_BOT_TOKEN", "")

bot = discord.Bot(intents=intents)

# Main bot code
# -------------------------------------
# =========================================================
# General
# =========================================================



# =========================================================
# Community Section
# =========================================================

# Blame Chatter
# -------------------------------------
@bot.slash_command(
    name="blame",
    description="Blame a chatter",
    guild_ids=[discord_main_guild_id]
)
async def blame(ctx, name):
    blame_percentage = random.randint(1, 100)
    await ctx.respond(str(name) + " is " + str(blame_percentage) + "%" + " to be blamed!")

# Cute Chatter
# -------------------------------------
@bot.slash_command(
    name="cute",
    description="Check how cute a chatter is!",
    guild_ids=[discord_main_guild_id]
)
async def blame(ctx, name):
    cute_percentage = random.randint(1, 100)
    await ctx.respond(str(name) + " is " + str(cute_percentage) + "%" + " cute today!")

# Sus Chatter
# -------------------------------------
@bot.slash_command(
    name="sus",
    description="Check how sus a chatter is!",
    guild_ids=[discord_main_guild_id]
)
async def blame(ctx, name):
    sus_percentage = random.randint(1, 100)
    await ctx.respond(str(name) + " is " + str(sus_percentage) + "%" + " sus today!")



# =========================================================
# RP Section
# =========================================================
# RP constants
base_character = Character()
CHARACTER_RACES = base_character.RACES
CHARACTER_GENDERS = base_character.GENDERS
CHARACTER_STATS = base_character.STATS
CHARACTER_ROLES = base_character.ROLES



# Autocomplete character races
# -------------------------------------
async def get_character_races(ctx: discord.AutocompleteContext):
    return [race for race in CHARACTER_RACES if race.startswith(ctx.value.lower())]

# Autocomplete character genders
# -------------------------------------
async def get_character_genders(ctx: discord.AutocompleteContext):
    return [gender for gender in CHARACTER_GENDERS if gender.startswith(ctx.value.lower())]

# Autocomplete character stats
# -------------------------------------
async def get_character_stats(ctx: discord.AutocompleteContext):
    return [stat for stat in CHARACTER_STATS if stat.startswith(ctx.value.lower())]

# Autocomplete character roles
# -------------------------------------
async def get_character_roles(ctx: discord.AutocompleteContext):
    return [role for role in CHARACTER_ROLES if role.startswith(ctx.value.lower()) and role != "Any"]



# Create a new RP character
# -------------------------------------
@bot.slash_command(
    name="create_character",
    description="Create your RP character in this server",
    guild_ids=[discord_main_guild_id]
)
@option("name", description="Your character's first name")
@option("surname", description="Your character's family name")
@option("race", description="Your character's race", autocomplete=get_character_races)
@option("gender", description="Your character's gender", autocomplete=get_character_genders)
@option("role", description="Your character's role (Class / Job)", autocomplete=get_character_roles)
@option("nsfw", description="Is your character nsfw or sfw (assumed: sfw)")
async def create_character(ctx, name: str, surname: str, race: str, gender: str, role: str, nsfw: bool):
    user_id = ctx.author.id

    # Check if the user already has a character
    test_char = Character()
    test_char = test_char.load(user_id)

    if test_char != Character().NO_CHARACTER_FOUND_ERROR:
        # Character already present
        await ctx.response.send_message(f"You already created a character with name: {test_char.get_name()}", ephemeral=True)

    else:
        # Check param inputs
        if race not in CHARACTER_RACES:
            await ctx.response.send_message(f"Race currently unsupported! Pick another one.", ephemeral=True)
            return
        
        if gender not in CHARACTER_GENDERS:
            await ctx.response.send_message(f"Pick a gender from the selected list.", ephemeral=True)
            return

        if role not in CHARACTER_ROLES:
            await ctx.response.send_message(f"Role not supported.", ephemeral=True) 
            return
        
        # Can create the character
        character = Character()
        character.create(name, surname, race, gender, nsfw)
        character.set_entity_id(user_id)
        character.set_role(role)

        await ctx.response.send_message(
            "Perfect! Your character will be epic I can already feel it!\n" + 
            character.describe() + "\n\n" +
            "I'm now going to roll for your stats. Don't worry you can assign those later~", ephemeral=True)
        
        # Roll for stats
        results = character.roll_stats()

        await ctx.followup.send(
            "Your rolls are as follow~ \n\n" +
            "" + str(results[0]) + " - " + str(results[1]) + " - " + str(results[2]) + "" + "\n" +
            "" + str(results[3]) + " - " + str(results[4]) + " - " + str(results[5]) + "" + "\n" +
            "Only the highest numbers will be taken for your stats!",
            ephemeral=True
        )

        await ctx.followup.send(f"Your character has been created and saved!.", ephemeral=True)



# Delete a character
# -------------------------------------
@bot.slash_command(
    name="delete_character",
    description="Delete your RP character in this server (This can't be reversed)",
    guild_ids=[discord_main_guild_id]
)
async def delete_character(ctx):
    user_id = ctx.author.id

    # Check if the user already has a character
    character = Character()
    character = character.load(user_id)

    if character != character.NO_CHARACTER_FOUND_ERROR:
        character.delete(user_id)
        await ctx.response.send_message("Your character has been deleted. Now you can create a new one.", ephemeral=True)
    else:
        await ctx.response.send_message(character.NO_RP_CHARACTER_ERROR, ephemeral=True)



# Assign RAW RP character stats
# -------------------------------------
@bot.slash_command(
    name="set_character_stats_order",
    description="Allocate your RAW stats from the initial character rolls following a stat precedence setup",
    guild_ids=[discord_main_guild_id]
)
@option("first_stat", description="Your highest stat", autocomplete=get_character_stats)
@option("second_stat", description="Your second highest stat", autocomplete=get_character_stats)
@option("third_stat", description="Your third highest stat", autocomplete=get_character_stats)
@option("fourth_stat", description="Your highest stat", autocomplete=get_character_stats)
@option("fifth_stat", description="Your highest stat", autocomplete=get_character_stats)
@option("sixth_stat", description="Your highest stat", autocomplete=get_character_stats)
async def set_character_stats_order(ctx, first_stat: str, second_stat: str, third_stat: str, fourth_stat: str, fifth_stat: str, sixth_stat: str):
    check_array = [
        first_stat,
        second_stat,
        third_stat,
        fourth_stat,
        fifth_stat,
        sixth_stat
    ]

    for stat in check_array:
        if stat not in CHARACTER_STATS:
            await ctx.response.send_message("The stat name entered is not valid", ephemeral=True)
            return
    
    user_id = ctx.author.id
    character = Character()
    character = character.load(user_id)

    # Character existence check
    if character != character.NO_CHARACTER_FOUND_ERROR:
        character.set_raw_stat(0, first_stat, False)
        character.set_raw_stat(1, second_stat, False)
        character.set_raw_stat(2, third_stat, False)
        character.set_raw_stat(3, fourth_stat, False)
        character.set_raw_stat(4, fifth_stat, False)
        character.set_raw_stat(5, sixth_stat, False)
        character.set_raw_stat(0, "", True)

        character.calc_stats()

        await ctx.response.send_message("RAW Stat composition assigned: " + str(character.get_stats()), ephemeral=True)

    else:
        await ctx.response.send_message(character.NO_RP_CHARACTER_ERROR, ephemeral=True)



# Assign RP character stats
# -------------------------------------
@bot.slash_command(
    name="set_character_stats",
    description="Allocate your unspent stats points",
    guild_ids=[discord_main_guild_id]
)
@option("stat_value", description="The stat value to add to your current (Note you need to have the points first)")
@option("character_stat", description="The stat to increase", autocomplete=get_character_stats)
async def set_character_stats(ctx, stat_value: int, character_stat: str):
    if character_stat not in CHARACTER_STATS:
        await ctx.response.send_message("The stat name entered is not valid", ephemeral=True)
        return
    
    user_id = ctx.author.id
    character = Character()
    character = character.load(user_id)

    # Character existence check
    if character != character.NO_CHARACTER_FOUND_ERROR:

        # Check if the character has the stats they want to assign
        if character.get_stat_points() >= stat_value:
            character.set_stat(stat_value, character_stat)
            await ctx.response.send_message("Character stats assigned and saved!", ephemeral=True)

        else:
            await ctx.response.send_message("You lack that amount of stat points", ephemeral=True)

    else:
        await ctx.response.send_message(character.NO_RP_CHARACTER_ERROR, ephemeral=True)



# Check your RP Character
# -------------------------------------
@bot.slash_command(
    name="check_character",
    description="Check your RP Character status",
    guild_ids=[discord_main_guild_id]
)
@option("entity_id", description="Get info for the specified entity id")
@option("silent", description="Doesn't print your character and only give you info about your stats (Default: False)")
async def check_character(ctx, entity_id=None, silent=False):
    user_id = ctx.author.id

    if entity_id is None:
        entity_id = user_id
        entity_id = "@" + str(user_id)
        user_id = entity_id

    else:
        entity_id = str(entity_id)
    
    if entity_id.startswith('<'):
        entity_id = str(entity_id).replace('<', '').replace('>', '')
        entity = Character()

    elif entity_id.startswith('@'):
        entity = Character()

    else:
        entity = Enemy()

    entity = entity.load(entity_id)

    if type(entity) is not str:
        if entity.ent_type == 'Character':
            title = entity.name + " " + entity.surname
        else:
            title = entity.name + " entity_id: " + entity.entity_id

        #user_avatar = ctx.author.avatar
        embed = discord.Embed(
            title=title,
            description=entity.description,
            color=discord.Color.blurple()
        )
        embed.add_field(name="Main Stats", value="")
        embed.add_field(name="HP", value=str(entity.hp) + "/" + str(entity.mhp), inline=True)
        embed.add_field(name="AC", value=str(entity.ac), inline=True)
        #embed.add_field(name="Parameters", value="")
        embed.add_field(name="Strength", value=entity.stats['strength'], inline=True)
        embed.add_field(name="Dexterity", value=entity.stats['dexterity'], inline=True)
        embed.add_field(name="Constitution", value=entity.stats['constitution'], inline=True)
        embed.add_field(name="Intelligence", value=entity.stats['intelligence'], inline=True)
        embed.add_field(name="Wisdom", value=entity.stats['wisdom'], inline=True)
        embed.add_field(name="Charisma", value=entity.stats['charisma'], inline=True)
        embed.add_field(name="Current status", value="")
        if entity.get_combat_ready() == 0:
            embed.add_field(name="Exhausted", value="Can't battle and needs rest.", inline=True)
        
        embed.add_field(name="", value="====", inline=False)
        embed.add_field(name="Backstory", value="Is empty in here for now...", inline=False)
        embed.set_author(name="RP Char card")

        await ctx.response.send_message("Here's your character card!", embed=embed, ephemeral=silent)

        if entity.ent_type == 'Character' and entity.has_unspent_stats() == True:
            stat_points = entity.get_stat_points()
            raw_stat_points = entity.get_raw_stats()
            raw_stat_explain_string = ""

            await ctx.followup.send(
                "Hey! You have unspent stat points! \n\n" +
                f"You have {str(stat_points)} stat points and {str(raw_stat_points)} raw stats.\n" +
                "To assign these, use the /set_character_stats and /set_character_stats_order commands\n" +
                raw_stat_explain_string,
                ephemeral=True
            )


    else:
        await ctx.response.send_message(entity, ephemeral=False)



# Check your Character's inventory
# -------------------------------------
@bot.slash_command(
    name="check_inventory",
    description="Check your RP Character status",
    guild_ids=[discord_main_guild_id]
)
@option("entity_id", description="Get info for the specified entity id")
@option("silent", description="Doesn't print your character and only give you info about your stats (Default: False)")
async def check_inventory(ctx, entity_id=None, silent=False):
    user_id = ctx.author.id

    if entity_id is None:
        entity_id = user_id
        entity_id = "@" + str(user_id)
        user_id = entity_id

    else:
        entity_id = str(entity_id)
    
    if entity_id.startswith('<'):
        entity_id = str(entity_id).replace('<', '').replace('>', '')
        entity = Character()

    elif entity_id.startswith('@'):
        entity = Character()

    else:
        entity = Enemy()

    entity = entity.load(entity_id)

    if type(entity) is not str:
        if entity.ent_type == 'Character':
            title = entity.name + " " + entity.surname + " - Inventory"
        else:
            title = entity.name + " entity_id: " + entity.entity_id

        #user_avatar = ctx.author.avatar
        embed = discord.Embed(
            title=title,
            description='',
            color=discord.Color.blurple()
        )
        embed.add_field(name="Main Items", value="", inline=False)
        embed.add_field(name="===", value="", inline=False)
        embed.add_field(name="Gold", value=str(entity.inventory.items['gold']), inline=True)
        embed.add_field(name="EXP", value=str(entity.cur_exp) + "/" + str(entity.req_exp), inline=True)
        
        embed.add_field(name="Equipment", value="", inline=False)
        embed.add_field(name="===", value="", inline=False)
        embed.add_field(name='Main weapon', value=entity.inventory.items['equipment']['main_weapon']['name'], inline=True)
        embed.add_field(name='Head', value=entity.inventory.items['equipment']['head']['name'], inline=True)
        embed.add_field(name='Chest', value=entity.inventory.items['equipment']['chest']['name'], inline=True)
        embed.add_field(name='Arms', value=entity.inventory.items['equipment']['arms']['name'], inline=True)
        embed.add_field(name='Legs', value=entity.inventory.items['equipment']['legs']['name'], inline=True)
        embed.add_field(name='Necklace', value=entity.inventory.items['equipment']['necklace']['name'], inline=True)

        embed.add_field(name="Pouch", value="", inline=False)

        str_pouch = ""
        index = 1
        for item in entity.inventory.items['pouch']:
            str_pouch += str(index) + " - Name: " + str(item['name']) + " | Description: " + str(item['description']) + " | Drop rate: " + str(item['base_drop_rate']) + "\n"
            index += 1

        embed.add_field(name="===", value=str_pouch, inline=False)
        embed.set_author(name="RP Char card")

        await ctx.response.send_message("Here's your character's inventory!", embed=embed, ephemeral=silent)

        if entity.ent_type == 'Character' and entity.has_unspent_stats() == True:
            stat_points = entity.get_stat_points()
            raw_stat_points = entity.get_raw_stats()
            raw_stat_explain_string = ""

            await ctx.followup.send(
                "Hey! You have unspent stat points! \n\n" +
                f"You have {str(stat_points)} stat points and {str(raw_stat_points)} raw stats.\n" +
                "To assign these, use the /set_character_stats and /set_character_stats_order commands\n" +
                raw_stat_explain_string,
                ephemeral=True
            )


    else:
        await ctx.response.send_message(entity, ephemeral=False)



# Check your Character's inventory
# -------------------------------------
@bot.slash_command(
    name="check_abilities",
    description="Check your RP Character abilities",
    guild_ids=[discord_main_guild_id]
)
@option("silent", description="Doesn't print your character and only give you info about your stats (Default: False)")
async def check_abilities(ctx, silent=False):
    user_id = ctx.author.id

    entity_id = None

    if entity_id is None:
        entity_id = user_id
        entity_id = "@" + str(user_id)
        user_id = entity_id

    else:
        entity_id = str(entity_id)
    
    if entity_id.startswith('<'):
        entity_id = str(entity_id).replace('<', '').replace('>', '')
        entity = Character()

    elif entity_id.startswith('@'):
        entity = Character()

    else:
        entity = Enemy()

    entity = entity.load(entity_id)

    if type(entity) is not str:
        if entity.ent_type == 'Character':
            title = entity.name + " " + entity.surname + " - Ability list"
        else:
            title = entity.name + " entity_id: " + entity.entity_id

        #user_avatar = ctx.author.avatar
        embed = discord.Embed(
            title=title,
            description='',
            color=discord.Color.blurple()
        )
        embed.add_field(name="Abilities", value="", inline=False)

        string_result = []
        string_result_index = 0

        for item in entity.get_abilities():
            tmp_string = ""

            if item['type'] != '':
                ability_class = str(item['type']).split('_')[0]
                ability_type = str(item['type']).split('_')[1]

            else:
                ability_class = 'melee'
                ability_type = 'physical'

            tmp_string += "**" + str(item['name']) + "**  - " + " **[" + ability_class + " " + ability_type + "] [" + str(item['dice_roll']) + "]**" + "\n"
            tmp_string += item['description'] + "\n"
            tmp_string += "Buffs: " + str(item['positive_effects']) + "\n"
            tmp_string += "Debuffs: " + str(item['negative_effects']) + "\n"
            tmp_string += "===" + "\n\n"
        
            if string_result == []:
                string_result.append(tmp_string)
            
            elif (len(string_result[string_result_index]) + len(tmp_string)) < 1024:
                string_result[string_result_index] += tmp_string

            else:
                string_result_index += 1
                string_result.append(tmp_string)
                
        for item in string_result:
            embed.add_field(name="===", value=item, inline=False)

        embed.set_author(name="RP Char card")

        await ctx.response.send_message("Here's your character's ability list!", embed=embed, ephemeral=silent)

        if entity.ent_type == 'Character' and entity.has_unspent_stats() == True:
            stat_points = entity.get_stat_points()
            raw_stat_points = entity.get_raw_stats()
            raw_stat_explain_string = ""

            await ctx.followup.send(
                "Hey! You have unspent stat points! \n\n" +
                f"You have {str(stat_points)} stat points and {str(raw_stat_points)} raw stats.\n" +
                "To assign these, use the /set_character_stats and /set_character_stats_order commands\n" +
                raw_stat_explain_string,
                ephemeral=True
            )


    else:
        await ctx.response.send_message(entity, ephemeral=False)



# Rest your character
# -------------------------------------
@bot.slash_command(
    name="rp_rest",
    description="Make your character rest and restore their stats. (Can also levelup)",
    guild_ids=[discord_main_guild_id]
)
@option("silent", description="Doesn't print your character and only give you info about your stats (Default: False)")
async def rp_rest(ctx, silent=False):
    user_id = ctx.author.id
    character = Character()
    character = character.load(user_id)

    # Character existence check
    if character != character.NO_CHARACTER_FOUND_ERROR:
        character.rest()

        if character.pronoun_self == 'her':
            pron = 'she'
            poss_pron = 'herself'
        else:
            pron = 'he'
            poss_pron = 'himself'

        await ctx.response.send_message(f"*{character.name} finds a comfortable and safe place close by and allows {poss_pron} a good rest*\n" +
                                        f"  - {character.name} recovers as {pron} sleeps~", ephemeral=silent)

    else:
        await ctx.response.send_message(character.NO_RP_CHARACTER_ERROR, ephemeral=True)



# Perform an action using your character
# -------------------------------------
@bot.slash_command(
    name="rp_action",
    description="Cast an ability using your RP character",
    guild_ids=[discord_main_guild_id]
)
@option("ability_name", description="The action you want to perform (Most basic is \"Attack\")")
@option("target", description="The target of the action (Depends on action - Empty = Self)")
@option("hide_rolls", description="If you want the rolls ro show or no, (Default = False)")
async def rp_action(ctx, ability_name: str, target=None, hide_rolls = False):
    user_id = '@' + str(ctx.author.id)
    character = Character()
    character = character.load(user_id)
    character_ability_res = ''
    encounter = False
    turn_end = False
    encounter_ended = False

    # Character exists or no (Can't do action if not exist)
    if character != Character().NO_CHARACTER_FOUND_ERROR:
        target_self = False
        target_user = False

        # If target is empty then target is self
        target = str(target)

        if target is None or target == 'None':
            target_self = True
            target = str(user_id)

        else:
            if '<' in target:
                target_user = True
                target = target.replace('<', '').replace('>', '')

        if target_self:
            # User case
            target_character = character

        elif target_user:
            target_character = Character()
            target_character = target_character.load(target)
        
        else:
            # Enemy case
            db_entities = character.get_entities('Enemy', target)

            if db_entities != []:
                target_character = Enemy()
                target_character = target_character.load(target)

            else:
                # Didn't find the enemy
                await ctx.response.send_message(Character().NO_RP_CHARACTER_ERROR, ephemeral=True)
                return
        

        # Check if the target is in another encounter
        if target_character.get_encounter_id() != 0:
            if character.get_encounter_id() == 0 or character.get_encounter_id() != target_character.get_encounter_id():
                character_ability_res = "That target is in another battle already and you're not part of it!"
                await ctx.response.send_message(character_ability_res, ephemeral=False)
                return
            
            else:
                encounter =True

        # Check if it is in an encoutner
        if character.get_encounter_id() != 0:
            if character.get_turn_ready() == 0:
                character_ability_res = "can't do any more actions this turn"

            else:
                character.set_turn_ready(0)
                encounter = Encounter()
                encounter.load(character.get_encounter_id())

                if encounter.check_end_turn():
                    turn_end = True

                character_ability_res = character.use_ability(ability_name, [target_character])

        else:
            character_ability_res = character.use_ability(ability_name, [target_character])


        if type(character_ability_res) == str:
            await ctx.response.send_message(f"{character.name} {character_ability_res}", ephemeral=False)

        else:
            action_result = f"*{character_ability_res[0][1]["cast"]}!*\n"

            # For each target in the skill result
            for ability_result in character_ability_res:
                target_name = ability_result[0][0]
                result = ability_result[0][1]
                roll_explain = ability_result[0][3]
                lines = ability_result[1]

                if roll_explain != '' and hide_rolls == False:
                    action_result = action_result + "\n" + roll_explain + "\n"

                if result == "success":
                    enemy_action_result = ability_result[0][4]
                    action_result = action_result + "  - " + lines["success"] + "\n\n" + enemy_action_result
                
                elif result == "success_win":
                    action_result = action_result + "  - " + lines["success"] + "\n"
                    encounter_ended = True

                elif result == "fail":
                    enemy_action_result = ability_result[0][4]
                    action_result = action_result + "  - " + lines["fail"] + "\n\n" + enemy_action_result
                
                else:
                    action_result = action_result + "  - " + target_name + " Cannot continue to fight...\n"

                if result == "success_win":
                    action_result = action_result + "  - " + target_name + " was defeated!\n"

            
            if encounter:
                if encounter_ended:
                    encounter.finish()
                else:
                    if turn_end:
                        action_result += "The turn has ended and a new one started!\n"
                        encounter.start_turn()

            # Print the action results
            await ctx.response.send_message(f"{action_result}", ephemeral=False)

    else:
        await ctx.response.send_message(Character().NO_RP_CHARACTER_ERROR, ephemeral=True)



# Spawn a random enemy
# -------------------------------------
@bot.slash_command(
    name="rp_enemy_spawn",
    description="Spawns a random enemy",
    guild_ids=[discord_main_guild_id]
)
@option("level", description="Enemy level")
@option("name", description="Enemy name")
@option("race", description="Enemy race", autocomplete=get_character_races)
@option("gender", description="Enemy gender", autocomplete=get_character_genders)
@option("role", description="Enemy role (Class / Job)", autocomplete=get_character_roles)
@option("nsfw", description="Is your character nsfw or sfw (assumed: sfw)")
async def rp_enemy_spawn(ctx, level = None, name = None, race = None, gender = None, role = None, nsfw = False):
    author = ctx.author
    user_id = ctx.author.id
    gm_role = discord.utils.find(lambda r: r.name == 'GM', ctx.guild.roles)
    
    if gm_role not in author.roles:
        await ctx.response.send_message("You are not a GM so can't spawn enemies!", ephemeral=False)
        return

    # Create a new enemy
    enemy_id = 0
    enemy = Enemy()

    # Find a new id
    db_enemies = enemy.get_entities('Enemy')

    if db_enemies != []:
        for db_enemy in db_enemies:
            if enemy_id < int(db_enemy['uid']):
                enemy_id = int(db_enemy['uid'])

    enemy_id += 1

    enemy = enemy.create(level, name, race, gender, role, nsfw)
    enemy.set_entity_id(str(enemy_id))
    enemy.rest()
    embed = discord.Embed(
        title=enemy.name + " " + enemy.surname + " - level [" + str(enemy.char_level) + "]" + " id: [" + str(enemy.entity_id) + "]",
        description=enemy.description,
        color=discord.Color.blurple()
    )
    embed.add_field(name="Main Stats", value="")
    embed.add_field(name="HP", value=str(enemy.hp) + "/" + str(enemy.mhp), inline=True)
    embed.add_field(name="AC", value=str(enemy.ac), inline=True)
    embed.add_field(name="Strength", value=enemy.stats['strength'], inline=True)
    embed.add_field(name="Dexterity", value=enemy.stats['dexterity'], inline=True)
    embed.add_field(name="Constitution", value=enemy.stats['constitution'], inline=True)
    embed.add_field(name="Intelligence", value=enemy.stats['intelligence'], inline=True)
    embed.add_field(name="Wisdom", value=enemy.stats['wisdom'], inline=True)
    embed.add_field(name="Charisma", value=enemy.stats['charisma'], inline=True)
    embed.add_field(name="Backstory", value="Is empty in here for now...")
    embed.set_author(name="RP Char card")

    await ctx.response.send_message("Here's your new generated enemy!\nUse the enemy_id when using action to target this enemy.", embed=embed, ephemeral=False)


# Start a battle
# -------------------------------------
@bot.slash_command(
    name="rp_battle_start",
    description="Start a battle",
    guild_ids=[discord_main_guild_id]
)
@option("party_list", description="List of character id in the encounter")
@option("enemy_list", description="List of enemy id in the encounter")
async def rp_battle_start(ctx, party_list: str, enemy_list: str):
    author = ctx.author
    user_id = ctx.author.id
    gm_role = discord.utils.find(lambda r: r.name == 'GM', ctx.guild.roles)
    
    if gm_role not in author.roles:
        await ctx.response.send_message("You are not a GM so can't start a battle!", ephemeral=True)
        return
    
    try:
        encounter = Encounter()
        encounter.create('Battle', party_list, enemy_list)


    except Exception as e:
        print("Battle creation failed!" + str(e))
        await ctx.response.send_message("Battle creation failed!", ephemeral=True)
        return


    await ctx.response.send_message("Battle started between " + str(encounter.enemy_party) + " and " + str(encounter.friendly_party), ephemeral=False)
    return


# Roll a dice (DnD style)
# -------------------------------------
@bot.slash_command(
name="roll_dice",
description="Roll a dice! Allowed types are d4, d6. d8, d10, d12 and d20",
guild_ids=[discord_main_guild_id]
)
async def roll_dice(ctx, dice_type, quantity):
    user_id = ctx.author.id

    dice = Dice(dice_type)
    character = Character()
    character = character.load(user_id)
    result = []

    if character != character.NO_CHARACTER_FOUND_ERROR:
        # Roll by using the character
        result = character.roll_dice(dice_type, quantity)

    else:
        dice = Dice(dice_type)
        result = dice.roll(quantity)


    if int(quantity) == 1:
        response = "The result of your " + quantity + dice_type + " roll is: " + str(result) + "!"

    else:
        str_result = str(result)
        for number in result:
            if number != max(result):
                str_result = str_result.replace(str(number), '\u0336' + str(number) + '\u0336')

        response = "The result of your " + quantity + dice_type + " roll is: " + str_result + "!"

    await ctx.respond(response)



# Run bot
# -------------------------------------
bot.run(token)