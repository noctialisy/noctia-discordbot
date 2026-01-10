# Main imports
# -------------------------------------
import os, json, random, discord
from discord.ext import commands
from discord.commands import option


# Game imports
# -------------------------------------
from game_classes.GameSystem import GameSystem
from game_classes.Character import Character
from game_classes.Dice import Dice

# Main bot code
# -------------------------------------
with open('./settings.json', 'r', encoding='utf-8') as settings_file:


    # Main variables and bot intents
    # -------------------------------------
    settings = json.load(settings_file) # Load settings file, if this fails the bot won't start
    discord_test_guild_id = settings["discord.test.guild.id"]
    discord_main_guild_id = settings["discord.main.guild.id"]
    token = settings["discord.bot.token"]
    intents = discord.Intents.all()
    bot = discord.Bot(intents=intents)


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
    CHARACTER_RACES = Character.RACES
    CHARACTER_GENDERS = Character.GENDERS
    CHARACTER_STATS = Character.STATS



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
    @option("nsfw", description="Is your character nsfw or sfw (assumed: sfw)")
    async def create_character(ctx, name: str, surname: str, race: str, gender: str, nsfw: bool):
        user_id = ctx.author.id

        # Check if the user already has a character
        test_char = GameSystem.load_character(user_id)

        if test_char != "Character not found or not loaded":
            await ctx.response.send_message(f"You already created a character with name: {test_char.get_name()}", ephemeral=True)

        else:
            character = Character()
            creation_result = character.create(name, surname, race, gender, nsfw)

        if not "success" in creation_result:
            await ctx.response.send_message("Character creation failed, please retry.", ephemeral=True)

        else:
            # To Do
            # Make player add background story (optional)
            # Ask if they want their server nickname changed to their char name (optional)

            await ctx.response.send_message(
                "Perfect! Your character will be epic I can already feel it!\n" + 
                character.describe() + "\n\n" +
                "I'm now going to roll for your stats. Don't worry you can change those later~", ephemeral=True)

            dice = Dice("d6")
            roll = 0
            results = []
            result_values = []

            while roll < 6:
                rolled = dice.roll(4)
                result = sum(sorted(rolled)[-3:])
                results.append(str(rolled) + "(" + str(result) + ")")
                result_values.append(result)

                roll += 1

            option_roles = ["Mage", "Warrior"]
            str_option_roles = str(option_roles)

            await ctx.followup.send(
                "Your rolls are as follow~ \n\n" +
                "" + str(results[0]) + " - " + str(results[1]) + " - " + str(results[2]) + "" + "\n" +
                "" + str(results[3]) + " - " + str(results[4]) + " - " + str(results[5]) + "" + "\n" +
                "Only the highest numbers will be taken for your stats!\n\n" +
                f"What role do you want to pick for your character? (Available starting roles: {str_option_roles}. Prepend with \"!\")",
                ephemeral=True
            )

            result_values.sort(reverse=True)
            character.set_raw_stats(result_values)


            while True:
                msg = await bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel.id == ctx.channel.id and msg.content.startswith("!"), timeout=15)
                character_role = str(msg.content).replace("!", "")

                # Remove the message
                await msg.delete()

                await ctx.followup.send(f"Perfect you have chosen to start as a {character_role}!.", ephemeral=True)
                character.set_role(character_role)
                
                GameSystem.save_character(user_id, character)
                await ctx.followup.send(f"Your character has been created and saved!.", ephemeral=True)
                break

    


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
        character = GameSystem.load_character(user_id)

        if character != "Character not found or not loaded":
            GameSystem.delete_character(user_id)
            await ctx.response.send_message("Your character has been deleted. Now you can create a new one.", ephemeral=True)
        else:
            await ctx.response.send_message("You don't have a RP character currently.", ephemeral=True)
    
    
    
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
        character = GameSystem.load_character(user_id)

        # Character existence check
        if character != "Character not found or not loaded":
            character.set_raw_stat(0, first_stat, False)
            character.set_raw_stat(1, second_stat, False)
            character.set_raw_stat(2, third_stat, False)
            character.set_raw_stat(3, fourth_stat, False)
            character.set_raw_stat(4, fifth_stat, False)
            character.set_raw_stat(5, sixth_stat, False)
            character.set_raw_stat(0, "", True)

            character.calc_stats()

            GameSystem.save_character(user_id, character)
            await ctx.response.send_message("RAW Stat composition assigned: " + str(character.get_stats()), ephemeral=True)

        else:
            await ctx.response.send_message("You don't have a RP character currently.", ephemeral=True)



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
        character = GameSystem.load_character(user_id)

        # Character existence check
        if character != "Character not found or not loaded":

            # Check if the character has the stats they want to assign
            if character.get_stat_points() >= stat_value:
                character.set_stat(stat_value, character_stat)
                GameSystem.save_character(user_id, character)
                await ctx.response.send_message("Character stats assigned and saved!", ephemeral=True)

            else:
                await ctx.response.send_message("You lack that amount of stat points", ephemeral=True)

        else:
            await ctx.response.send_message("You don't have a RP character currently.", ephemeral=True)



    # Check your RP Character
    # -------------------------------------
    @bot.slash_command(
        name="check_character",
        description="Check your RP Character status",
        guild_ids=[discord_main_guild_id]
    )
    @option("silent", description="Doesn't print your character and only give you info about your stats (Default: False)")
    async def check_character(ctx, silent=False):
        user_id = ctx.author.id
        character = GameSystem.load_character(user_id)

        if character != "Character not found or not loaded":
            await ctx.response.send_message(str(character.describe()), ephemeral=silent)

            if character.has_unspent_stats() == True:
                stat_points = character.get_stat_points()
                raw_stat_points = character.get_raw_stats()
                raw_stat_explain_string = ""

                await ctx.followup.send(
                    "Hey! You have unspent stat points! \n\n" +
                    f"You have {str(stat_points)} stat points and {str(raw_stat_points)} raw stats.\n" +
                    "To assign these, use the /set_character_stats and /set_character_stats_order commands\n" +
                    raw_stat_explain_string,
                    ephemeral=True
                )


        else:
            await ctx.response.send_message("You don't have a RP character currently.", ephemeral=False)


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
        character = GameSystem.load_character(user_id)

        # Character existence check
        if character != "Character not found or not loaded":
            character.rest()
            GameSystem.save_character(user_id, character)

            await ctx.response.send_message("You find a comfortable and safe place close by and allow yourself a few moments of respite\n\n" +
                                            "You wake up fully rested!", ephemeral=silent)

        else:
            await ctx.response.send_message("You don't have a RP character currently.", ephemeral=True)
    
    
    # Cast and ability using your character
    # -------------------------------------
    @bot.slash_command(
        name="rp_cast",
        description="Cast an ability using your RP character",
        guild_ids=[discord_main_guild_id]
    )
    @option("ability_name", description="The ability you want to cast")
    @option("target", description="The target of the ability (Optional)")
    async def rp_cast(ctx, ability_name: str, target = None):
        user_id = ctx.author.id
        character = GameSystem.load_character(user_id)

        if character != "Character not found or not loaded":
            target = str(target).replace("@", "").replace("<", "").replace(">", "")

            files = os.listdir('./game_saves')
            is_user = False

            for file_name in files:
                if target in file_name:
                    is_user = True
                    break


            if is_user:
                target_character = GameSystem.load_character(target)

                if target_character == "Character not found or not loaded":
                    await ctx.response.send_message("It seems that the target of this command is a discord member, but they don't have a character yet.", ephemeral=False)
                    return
                
                else:
                    character_ability_res = character.use_ability(ability_name, target_character)

                    if type(character_ability_res) == str:
                        await ctx.response.send_message(f"{character.name} {character_ability_res}", ephemeral=False)

                    else:
                        await ctx.response.send_message(f"{character.name} {character_ability_res[1]["cast"]}!", ephemeral=False)

                        if character_ability_res[0] == "success":
                            await ctx.followup.send(f"{character_ability_res[1]["success"]}", ephemeral=False)

                        else:
                            await ctx.followup.send(f"{character_ability_res[1]["fail"]}", ephemeral=False)


        else:
            await ctx.response.send_message("You don't have a RP character currently.", ephemeral=True)

    
    
    # Roll a dice (DnD style)
    # -------------------------------------
    @bot.slash_command(
    name="roll_dice",
    description="Roll a dice! Allowed types are d4, d6. d8, d10, d12 and d20",
    guild_ids=[discord_main_guild_id]
    )
    async def roll_dice(ctx, dice_type, quantity):
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