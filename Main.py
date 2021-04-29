#   v0.0.6

import discord
from discord.ext import commands
import json
import os
import asyncio
import random

token = "ODE5OTQ3NDc4ODQ0NTcxNzQ5.YEuBmA.p0DzO32bCD5LbWeOPrqcbnd-Ebc"
os.chdir(r"C:\Users\danie\PycharmProjects\yt_vid_downloading\remind_bot")
intents = discord.Intents.all()
version = "v0.0.6"
link = "https://discord.com/api/oauth2/authorize?client_id=819947478844571749&permissions=8&scope=bot"
prefix_ = "r,"
bot = commands.Bot(command_prefix=prefix_, intents=intents)
bot.remove_command('help')

global tips
tips = ["Tip: Can't beat a dungeon or boss? Try obtaining a healing item!",
        "Tip: Enemy stats are dependant on your own: don't expect everything to always be easy!",
        "Tip: Need to get stronger? Level up by battling other people!",
        "Tip: Defending does not help you if you have no armor!",
        "Tip: If the bot stops responding, wait a few seconds and react again.",
        "Tip: Find a bug? Report it to the Pyfever team at https://discord.gg/TXR3hSkf. It is much appreciated!"]


# events

@bot.event
async def on_ready():
    print('{0.user} is ready for battle!'.format(bot))

    activity = discord.Game(name="in a battle }{ r,", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title='ERROR',
                           description="❓ You forgot to type something!",
                           color=discord.Color.red())
        await ctx.send(embed=em)
        ctx.command.reset_cooldown(ctx)
    elif isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title='ERROR', description="✖️ That command does not exist!", color=discord.Color.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.UserInputError):
        em = discord.Embed(title='ERROR', description="😵 You mistyped something!", color=discord.Color.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title='ERROR',
                           description="🔐 You lack the permissions to use that command!", color=discord.Color.red())
        await ctx.send(embed=em)


@bot.event
async def on_message(message):
    # if the message author is the bot, it does not respond
    if message.author == bot.user:
        return
    if message.author.bot:
        return

    await bot.process_commands(message)


# commands

# general commands

@bot.command(aliases=['commands', 'how'])
async def help(ctx):
    em = discord.Embed(title="Commands", color=discord.Color.dark_blue())
    em.add_field(name="***help, commands, how***", value="displays this message", inline=False)
    em.add_field(name="***profile, user, me***", value="opens your profile", inline=False)
    em.add_field(name="***info, rpg, bot***", value="displays bot information", inline=False)
    em.add_field(name="***battle, practice, spar***", value="starts a battle with the bot", inline=False)
    em.add_field(name="***quest, dungeon, adventure***", value="begins a quest", inline=False)
    await ctx.send(embed=em)


@bot.command(aliases=['rpg', 'bot'])
async def info(ctx):
    em = discord.Embed(title="Bot Information",
                       description="RPG is a bot developed for battling with friends and against the bot.",
                       color=discord.Color.dark_gold())
    em.add_field(name="**Version**", value=version, inline=False)
    em.add_field(name="**Language**", value="Python", inline=False)
    em.add_field(name="**Date of Creation**", value="April 20, 2021", inline=False)
    em.add_field(name="**Devs**", value="The PyFever team", inline=False)
    await ctx.send(embed=em)


# user profiles

async def open_profile(user):
    users = await get_profile()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["hp"] = 100
        users[str(user.id)]["armor"] = 0
        users[str(user.id)]["dmg"] = 20
        users[str(user.id)]["lvl"] = 1
        users[str(user.id)]["xp"] = 0
    with open("profiles.json", "w") as f:
        json.dump(users, f)
        return True


async def get_profile():
    with open("profiles.json", "r") as f:
        users = json.load(f)

        return users


async def update_profile(user, change=0, mode="hp"):
    users = await get_profile()

    users[str(user.id)][mode] += change

    with open("profiles.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]['hp'],
           users[str(user.id)]['armor'],
           users[str(user.id)]["dmg"],
           users[str(user.id)]["lvl"],
           users[str(user.id)]["xp"]]
    return bal


@bot.command(aliases=['me', 'user'])
async def profile(ctx):
    await open_profile(ctx.author)

    user = ctx.author

    users = await get_profile()

    hp_amt = users[str(user.id)]["hp"]
    armor_rating = users[str(user.id)]["armor"]
    atk = users[str(user.id)]["dmg"]
    level = users[str(user.id)]["lvl"]
    exp = users[str(user.id)]["xp"]

    em = discord.Embed(title=f"{ctx.author.name}'s Profile (Level " + str(level) + ")", color=discord.Color.blue())
    em.add_field(name="**Health**", value=str(hp_amt))
    em.add_field(name="**Armor**", value=str(armor_rating))
    em.add_field(name="**Attack**", value=str(atk))
    em.add_field(name="**Experience**", value=str(exp))
    await ctx.send(embed=em)


# bot battling

@bot.command(aliases=['practice', 'spar'])
async def battle(ctx):
    emoji1 = '🗡️'
    emoji2 = '🛡️'
    emoji3 = '❌'

    bot_hp = 100

    await open_profile(ctx.author)
    user = ctx.author
    users = await get_profile()

    hp_amt = users[str(user.id)]["hp"]
    atk = users[str(user.id)]["dmg"]
    armor_rating = users[str(user.id)]["armor"]

    em = discord.Embed(title="Practice Battle", color=discord.Color.orange())
    em.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
    em.add_field(name="RPG(bot)", value=str(bot_hp) + " HP")
    em.set_footer(
        text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")
    x = await ctx.send(embed=em)

    await x.add_reaction(emoji1)
    await x.add_reaction(emoji2)
    await x.add_reaction(emoji3)

    def check(reaction, user):
        return user == ctx.author and (reaction.message == x and str(reaction) == '🗡️' or str(reaction) == '🛡️' or str(reaction) == '❌')

    bot_defended = False
    turn = 'user'

    while bot_hp > 0 or hp_amt > 0:
        defended = False
        bot_armor = 0
        # user's turn
        if turn == 'user':
            if bot_defended is True:
                bot_armor = 5
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=600.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("The battle has timed out.")
                return
            else:
                if str(reaction) == '🗡️':
                    miss = random.randint(1, 6)
                    if miss == 5:
                        e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                        e.add_field(name=f"{ctx.author.name} *missed!*", value=str(hp_amt) + " HP")
                        e.add_field(name="RPG(bot)", value=str(bot_hp) + " HP")
                        e.set_footer(
                            text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")
                        await x.edit(embed=e)
                        await x.clear_reactions()
                        turn = 'bot'
                        continue
                    damage = random.randrange(5, atk + 5, 5) - int(bot_armor)
                    if damage < 0:
                        damage = 0
                    bot_hp -= damage

                    if bot_hp < 0:
                        bot_hp = 0

                    e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                    e.add_field(name=f"{ctx.author.name} *attacked!*", value=str(hp_amt) + " HP")
                    e.add_field(name="RPG(bot)", value='- **' + str(damage) + '** ' + str(bot_hp) + " HP")
                    e.set_footer(
                        text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")
                    await x.edit(embed=e)

                    if bot_hp <= 0:
                        e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                        e.add_field(name=f"{ctx.author.name} *wins!*", value=str(hp_amt) + " HP")
                        e.add_field(name="RPG(bot)", value='- **' + str(damage) + '** ' + str(bot_hp) + " HP")
                        await x.edit(embed=e)
                        break

                    bot_defended = False

                    await x.clear_reactions()

                    turn = 'bot'

                elif str(reaction) == '🛡️':
                    e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                    e.add_field(name=f"{ctx.author.name} *defended!*", value=str(hp_amt) + " HP")
                    e.add_field(name="RPG(bot)", value=str(bot_hp) + " HP")
                    e.set_footer(
                        text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")
                    await x.edit(embed=e)

                    defended = True

                    bot_defended = False

                    await x.clear_reactions()

                    turn = 'bot'

                elif str(reaction) == '❌':
                    await x.clear_reactions()
                    e = discord.Embed(title="Practice Battle Canceled",color=discord.Color.red())
                    e.set_footer(text=random.choice([tips[0], tips[1], tips[2], tips[3], tips[4], tips[5]]))

                    await x.edit(embed=e)
                    break

        # bot's turn

        if turn == 'bot':
            if defended is True:
                armor_rating += armor_rating*2

            action = random.choice(['attack', 'defend'])
            if action == 'attack':
                miss = random.randint(1, 6)
                if miss == 5:
                    e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                    e.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
                    e.add_field(name="RPG(bot) *missed!*", value=str(bot_hp) + " HP")
                    e.set_footer(
                        text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")
                    await x.edit(embed=e)
                    await x.add_reaction(emoji1)
                    await x.add_reaction(emoji2)
                    await x.add_reaction(emoji3)
                    turn = 'user'
                    continue

                damage = random.randrange(5, 30, 5) - int(armor_rating)
                if damage < 0:
                    damage = 0
                hp_amt -= damage

                if hp_amt < 0:
                    hp_amt = 0

                e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                e.add_field(name=f"{ctx.author.name}", value='- **' + str(damage) + '** ' + str(hp_amt) + " HP")
                e.add_field(name="RPG(bot) *attacked!*", value=str(bot_hp) + " HP")
                e.set_footer(
                    text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")
                await x.edit(embed=e)

                if hp_amt <= 0:
                    e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                    e.add_field(name=f"{ctx.author.name}", value='- **' + str(damage) + '** ' + str(hp_amt) + " HP")
                    e.add_field(name="RPG(bot) *wins!*", value=str(bot_hp) + " HP")
                    await x.edit(embed=e)
                    break

                await x.add_reaction(emoji1)
                await x.add_reaction(emoji2)
                await x.add_reaction(emoji3)

                turn = 'user'

            elif action == 'defend':
                e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
                e.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
                e.add_field(name="RPG(bot) *defended!*", value=str(bot_hp) + " HP")
                e.set_footer(
                    text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")
                await x.edit(embed=e)

                bot_defended = True

                await x.add_reaction(emoji1)
                await x.add_reaction(emoji2)
                await x.add_reaction(emoji3)

                turn = 'user'


# dungeons

@bot.command(aliases=['dungeon', 'adventure'])
async def quest(ctx):
    dungeon_name = random.choice(['Misty', 'Ominous', 'Old', 'Antiquated', 'Dark', 'Gloomy']) + ' ' + random.choice(['Corridors', 'Tower', 'Castle', 'Forest', 'Swamp', 'Dimension']) + ' of ' + random.choice(['Doom', 'Darkness', 'Evil', 'Sorrow', 'Confusion', 'Death', 'Yore'])

    room = 1
    progress = '🟨 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜'
    enemy = random.choice(['Elf', 'Skeleton', 'Orc', 'Knight', 'Goblin', 'Huge Wolf', 'Sorcerer', 'Angry Peasant'])

    emoji1 = '🗡️'
    emoji2 = '🛡️'
    emoji3 = '❌'

    bot_hp = 100

    await open_profile(ctx.author)
    user = ctx.author
    users = await get_profile()

    hp_amt = users[str(user.id)]["hp"]
    atk = users[str(user.id)]["dmg"]
    armor_rating = users[str(user.id)]["armor"]
    level = users[str(user.id)]["lvl"]

    color = discord.Color.random()

    em = discord.Embed(title=dungeon_name, description=progress, color=color)
    em.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
    em.add_field(name=enemy + ' *appeared!*', value=str(bot_hp) + " HP")
    em.set_footer(
        text="You are on a quest to defeat the leader of this domain!")
    x = await ctx.send(embed=em)

    await x.add_reaction(emoji1)
    await x.add_reaction(emoji2)
    await x.add_reaction(emoji3)

    def check(reaction, user):
        return user == ctx.author and (reaction.message == x and str(reaction) == '🗡️' or str(reaction) == '🛡️' or str(reaction) == '❌')

    bot_defended = False
    is_boss = False
    turn = 'user'

    while bot_hp > 0 or hp_amt > 0:
        defended = False
        bot_armor = atk//10
        # user's turn
        if turn == 'user':
            if bot_defended is True:
                bot_armor = bot_armor*2
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=600.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.name}'s quest has ended.")
                return
            else:
                if str(reaction) == '🗡️':
                    miss = random.randint(1, 6)
                    if miss == 5:
                        e = discord.Embed(title=dungeon_name, description=progress, color=color)
                        e.add_field(name=f"{ctx.author.name} *missed!*", value=str(hp_amt) + " HP")
                        e.add_field(name=enemy, value=str(bot_hp) + " HP")
                        e.set_footer(
                            text="You are on a quest to defeat the leader of this domain!")
                        await x.edit(embed=e)
                        await x.clear_reactions()
                        turn = 'bot'
                        continue
                    damage = random.randrange(5, atk + 5, 5) - int(bot_armor)
                    if damage < 0:
                        damage = 0
                    bot_hp -= damage

                    if bot_hp < 0:
                        bot_hp = 0

                    e = discord.Embed(title=dungeon_name, description=progress, color=color)
                    e.add_field(name=f"{ctx.author.name} *attacked!*", value=str(hp_amt) + " HP")
                    e.add_field(name=enemy, value='- **' + str(damage) + '** ' + str(bot_hp) + " HP")
                    e.set_footer(
                        text="You are on a quest to defeat the leader of this domain!")
                    await x.edit(embed=e)

                    if bot_hp <= 0:
                        if is_boss is True:
                            await x.clear_reactions()

                            e = discord.Embed(title=dungeon_name, description=progress, color=color)
                            e.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
                            e.add_field(name=enemy + ' *has been defeated!*',
                                        value='- **' + str(damage) + '** ' + str(bot_hp) + " HP")
                            await x.edit(embed=e)

                            await asyncio.sleep(3)

                            xp_gain = 25

                            w = discord.Embed(title="Victory!",
                                              description=f"{ctx.author.name} completed a quest!",
                                              color=discord.Color.gold())
                            w.add_field(name="Your reward:", value=str(xp_gain) + ' experience!')
                            await x.edit(embed=w)
                            break

                        e = discord.Embed(title=dungeon_name, description=progress, color=color)
                        e.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
                        e.add_field(name=enemy + ' *has been defeated!*',
                                    value='- **' + str(damage) + '** ' + str(bot_hp) + " HP")
                        await x.edit(embed=e)

                        await x.clear_reactions()

                        progress = progress.replace('⬜', '🟨', 1)
                        progress = progress.replace('🟨', '🟩', 1)

                        enemy = random.choice(
                            ['Elf', 'Skeleton', 'Orc', 'Knight', 'Goblin', 'Huge Wolf', 'Sorcerer', 'Angry Peasant'])

                        bot_hp = 100

                        if progress == "🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟨":
                            progress = '🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟥'

                        if progress == '🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟥':
                            is_boss = True
                            bot_hp = 100 + ((atk//2)*5)
                            if level >= 20:
                                enemy = random.choice(['God of Storms',
                                                       'Celestial Worm, Eater of Galaxies',
                                                       'Time God',
                                                       'The Great Serpent, Bringer of Dragons',
                                                       'Awakened Planet-Conqueror',
                                                       'God of the Undead'])
                            elif level >= 10:
                                enemy = random.choice(['Skeleton Lord',
                                                       'Orc War King',
                                                       'Goblin Grand Mage',
                                                       'Elf Dragon-slayer',
                                                       'Ancient Drake',
                                                       'Master Wizard',
                                                       'Celestial Worm Baby'])
                            else:
                                enemy = random.choice(['Giant',
                                                       'Armored Wolf-Rider',
                                                       'Wyvern',
                                                       'Elemental Warlock',
                                                       'Demon Executioner',
                                                       'Dark Knight',
                                                       'Horseback Spartan Chief'])

                        hp_amt = users[str(user.id)]["hp"]

                        room += 1

                        em = discord.Embed(title=dungeon_name, description=progress, color=color)
                        em.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
                        em.add_field(name=enemy + ' *appeared!*', value=str(bot_hp) + " HP")
                        em.set_footer(text="You are on a quest to defeat the leader of this domain!")
                        await x.edit(embed=em)

                        await x.add_reaction(emoji1)
                        await x.add_reaction(emoji2)
                        await x.add_reaction(emoji3)

                        continue

                    bot_defended = False

                    await x.clear_reactions()

                    turn = 'bot'

                elif str(reaction) == '🛡️':
                    e = discord.Embed(title=dungeon_name, description=progress, color=color)
                    e.add_field(name=f"{ctx.author.name} *defended!*", value=str(hp_amt) + " HP")
                    e.add_field(name=enemy, value=str(bot_hp) + " HP")
                    e.set_footer(
                        text="You are on a quest to defeat the leader of this domain!")
                    await x.edit(embed=e)

                    defended = True

                    bot_defended = False

                    await x.clear_reactions()

                    turn = 'bot'

                elif str(reaction) == '❌':
                    await x.clear_reactions()
                    e = discord.Embed(title="Quest Canceled", color=discord.Color.red())
                    e.set_footer(text=random.choice([tips[0], tips[1], tips[2], tips[3], tips[4], tips[5]]))

                    await x.edit(embed=e)
                    break

        # bot's turn

        if turn == 'bot':
            if defended is True:
                armor_rating += armor_rating * 2

            action = random.choice(['attack', 'defend'])
            if action == 'attack':
                miss = random.randint(1, 6)
                if miss == 5:
                    e = discord.Embed(title=dungeon_name, description=progress, color=color)
                    e.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
                    e.add_field(name=enemy + " *missed!*", value=str(bot_hp) + " HP")
                    e.set_footer(
                        text="You are on a quest to defeat the leader of this domain!")
                    await x.edit(embed=e)
                    await x.add_reaction(emoji1)
                    await x.add_reaction(emoji2)
                    await x.add_reaction(emoji3)
                    turn = 'user'
                    continue

                damage = random.randrange(5, hp_amt//5, 5) - int(armor_rating)
                if progress == '🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟥':
                    damage = random.randrange(5, (hp_amt//5)*2, 5) - int(armor_rating)

                if damage < 0:
                    damage = 0
                hp_amt -= damage

                if hp_amt < 0:
                    hp_amt = 0

                e = discord.Embed(title=dungeon_name, description=progress, color=color)
                e.add_field(name=f"{ctx.author.name}", value='- **' + str(damage) + '** ' + str(hp_amt) + " HP")
                e.add_field(name=enemy + " *attacked!*", value=str(bot_hp) + " HP")
                e.set_footer(
                    text="You are on a quest to defeat the leader of this domain!")
                await x.edit(embed=e)

                if hp_amt <= 0:
                    e = discord.Embed(title=dungeon_name, description=progress, color=color)
                    e.add_field(name=f"{ctx.author.name} has been slain.",
                                value='- **' + str(damage) + '** ' + str(hp_amt) + " HP")
                    e.add_field(name=enemy, value=str(bot_hp) + " HP")
                    e.set_footer(
                        text="The quest has ended.\n" + random.choice([tips[0], tips[1], tips[2], tips[3], tips[4], tips[5]]))
                    await x.edit(embed=e)
                    break

                await x.add_reaction(emoji1)
                await x.add_reaction(emoji2)
                await x.add_reaction(emoji3)

                turn = 'user'

            elif action == 'defend':
                e = discord.Embed(title=dungeon_name, description=progress, color=color)
                e.add_field(name=f"{ctx.author.name}", value=str(hp_amt) + " HP")
                e.add_field(name=enemy + " *defended!*", value=str(bot_hp) + " HP")
                e.set_footer(
                    text="You are on a quest to defeat the leader of this domain!")
                await x.edit(embed=e)

                bot_defended = True

                await x.add_reaction(emoji1)
                await x.add_reaction(emoji2)
                await x.add_reaction(emoji3)

                turn = 'user'


bot.run(token)

