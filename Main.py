#   v0.0.4

import discord
from discord.ext import commands
import json
import os
import random

token = "ODE5OTQ3NDc4ODQ0NTcxNzQ5.YEuBmA.IPV09eEIHnlKUszD3WSHPbCzhSA"
os.chdir(r"C:\Users\danie\PycharmProjects\yt_vid_downloading\remind_bot")
intents = discord.Intents.all()
version = "v0.0.4"
link = "https://discord.com/api/oauth2/authorize?client_id=819947478844571749&permissions=8&scope=bot"
prefix_ = "r,"
bot = commands.Bot(command_prefix=prefix_, intents=intents)
bot.remove_command('help')


# events

@bot.event
async def on_ready():
    print('{0.user} is ready for battle!'.format(bot))


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
    em.add_field(name="***info, rpg, bot***", value="starts a battle with the bot", inline=False)
    em.add_field(name="***battle, practice, spar***", value="displays bot information", inline=False)
    await ctx.send(embed=em)


@bot.command(aliases=['rpg', 'bot'])
async def info(ctx):
    em = discord.Embed(title="Bot Information",
                       description="RPG is a bot developed for battling with friends and against the bot.",
                       color=discord.Color.dark_gold())
    em.add_field(name="**Version**", value=version, inline=False)
    em.add_field(name="**Language**", value="Python", inline=False)
    em.add_field(name="**Date of Creation**", value="April 20, 2021", inline=False)
    em.add_field(name="**Dev**", value="Domtuber#1408", inline=False)
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
    exp = users[str(user.id)]["xp"]

    em = discord.Embed(title=f"{ctx.author.name}'s Profile", color=discord.Color.blue())
    em.add_field(name="**Health**", value=str(hp_amt))
    em.add_field(name="**Armor**", value=str(armor_rating))
    em.add_field(name="**Attack**", value=str(atk))
    em.add_field(name="**Experience**", value=str(exp))
    await ctx.send(embed=em)


# bot battling

@bot.command(aliases=['practice','spar'])
async def battle(ctx):
    emoji1 = '🗡️'
    emoji2 = '🛡️'

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

    def check(reaction, user):
        return user == ctx.author and (reaction.message == x and str(reaction) == '🗡️' or str(reaction) == '🛡️')

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("The battle has timed out.")
    else:
        if str(reaction) == '🗡️':
            miss = random.randint(1, 6)
            if miss == 5:
                await ctx.send(f"{ctx.author.name} missed!")
            damage = random.randrange(5, atk, 5)

            bot_hp -= damage

            e = discord.Embed(title="Practice Battle", color=discord.Color.orange())
            e.add_field(name=f"{ctx.author.name} *attacked!*", value=str(hp_amt) + " HP")
            e.add_field(name="RPG(bot)", value='- **' + str(damage) + '** ' + str(bot_hp) + " HP")
            e.set_footer(
                text="You are now in a practice battle with the bot! React with the sword to attack or the shield to defend.")

            await x.edit(embed=e)

        elif str(reaction) == '🛡️':
            await ctx.send('pp')


bot.run(token)
