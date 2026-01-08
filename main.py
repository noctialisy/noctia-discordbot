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
    settings = json.loads(settings_file) # Load settings file, if this fails the bot won't start
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
    CHARACTER_RACES = Character.CHARACTER_RACES
    CHARACTER_GENDERS = Character.CHARACTER_GENDERS

    # Autocomplete character races
    # -------------------------------------
    async def get_character_races(ctx: discord.AutocompleteContext):
        return [race for race in CHARACTER_RACES if race.startswith(ctx.value.lower())]

    # Autocomplete character genders
    # -------------------------------------
    async def get_character_genders(ctx: discord.AutocompleteContext):
        return [gender for gender in CHARACTER_GENDERS if gender.startswith(ctx.value.lower())]

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

            character.set_raw_stats(result_values)


            while True:
                msg = await bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel.id == ctx.channel.id, timeout=30)
                character_role = str(msg.content).replace("!", "")
                
                # Remove the message
                await msg.delete()

                await ctx.followup.send(f"Perfect you have chosen to start as a {character_role}!.", ephemeral=True)
                character.set_role(character_role)
                
                GameSystem.save_character(user_id, character)
                await ctx.followup.send(f"Your character has been created and saved!.", ephemeral=True)


    # Check your RP Character
    # -------------------------------------
    @bot.slash_command(
    name="check_character",
    description="Check your RP Character status",
    guild_ids=[discord_main_guild_id]
    )
    async def check_character(ctx):
        user_id = ctx.author.id
        character = GameSystem.load_character(user_id)

        if character != "Character not found or not loaded":
            await ctx.response.send_message(character.describe(), ephemeral=True)

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