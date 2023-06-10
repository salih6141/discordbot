import discord
from discord.ext import commands
import pymongo
import openai
import re
import config
import requests
import time
from discord.ext.music import MusicClient, Track, WAVAudio

openai.api_key = config.API_KEY
ENDPOINT_URL = 'https://api.openai.com/v1/chat/completions'
RATE_LIMIT = 40000
username = config.username
password = config.password
url = "mongodb+srv://<username>:<password>@discordbot.gltp06j.mongodb.net/?retryWrites=true&w=majority"

url = url.replace("<username>", username).replace("<password>", password)
# encoded_url = quote_plus(url)
pymongoClient = pymongo.MongoClient(url)

db = pymongoClient["DiscordBotDB"]
print('connection has been made to {collection}', db)
collection = db["Donut"]


def run_discord_bot():
    TOKEN = config.tokenkey
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="?", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        await bot.change_presence(activity=discord.Game('?help_me | bishes'))

    @bot.event
    async def on_message(message):
        if message.content.startswith('?') or message.content.startswith('.'):
            print(f'{message.author}: {message.content}')
        # this code allows for specific users (redstone-torch, Powered-Rail) to add a donut by tagging another user
        if message.content.startswith(
                '.he is a donut') and message.author.id == 308367178715889664 or message.content.startswith(
            '.he is a donut') and message.author.id == 364456382185078806:
            query = {'id': f"{message.mentions[0].id}"}
            f = collection.find_one(query)
            if f:
                new_value = {'$inc': {'donutCounter': 1}}
                collection.update_one(query, new_value)
                x = collection.find({'id': message.author.id})
                await message.channel.send(f'```Thank you for informing me that {message.mentions[0]} is a failure.```')
            else:
                await message.channel.send(f'```This user has not yet been added to the database.```')
        if message.content.startswith(
                '.he is a donut') and message.author.id != 308367178715889664 or message.content.startswith(
            '.he is a donut') and message.author.id == 364456382185078806:
            await message.channel.send(f'YOU DO NOT HAVE THE PRIVILIGE. also you a snitch')
        # end section

        # this section takes care of the aceCounter and also the restriction on user giving themselves an ace
        if message.content.startswith('.') and message.content.endswith('got an ace') and message.mentions[
            0].id != message.author.id:
            query = {'id': f"{message.mentions[0].id}"}
            f = collection.find_one(query)
            if f:
                new_value = {'$inc': {'aceCounter': 1}}
                collection.update_one(query, new_value)
                x = collection.find({'id': message.author.id})
                await message.channel.send(f'```{message.mentions[0]} has aced!!```')
            else:
                await message.channel.send(f'```This user has not yet been added to the database.```')

        if message.content.startswith('.') and message.content.endswith('got an ace') and message.mentions[
            0].id == message.author.id:
            await message.channel.send(f'```Users are NOT allowed to give an ace to themselves. It must be given by '
                                       f'another user that was present during the ace!```')
        # end section

        # this code allows for users to mark another user as a bitch
        if message.content.endswith('is a bitch') and message.content.startswith('.'):
            query = {'id': f"{message.mentions[0].id}"}
            f = collection.find_one(query)
            if f:
                new_value = {'$inc': {'bitchCounter': 1}}
                collection.update_one(query, new_value)
                x = collection.find({'id': message.author.id})
                await message.channel.send(f'```{message.mentions[0]} Has been called out for being a BITCH!```')
            else:
                await message.channel.send(f'```This user has not yet been added to the database.```')
        # end section

        # this code deals with adding a teamkill and recording the last person the user teamkilled
        if message.content.startswith('.teamkill') and message.mentions[0].id != message.mentions[1].id:
            query = {'id': f"{message.mentions[0].id}"}
            f = collection.find_one(query)
            if f:
                new_value = {'$inc': {'teamkillCounter': 1}}
                new_value2 = {'$set': {'teamkilled': f'{message.mentions[1]}'}}
                collection.update_one(query, new_value)
                collection.update_one(query, new_value2)
                await message.channel.send(f'```{message.mentions[0]} has just teamkilled {message.mentions[1]}.```')
            else:
                await message.channel.send(f'```There is something wrong with your command!```')

        # this code allows the user to add a donut to themselves
        if message.content.startswith('.i suck'):
            query = {'id': f"{message.author.id}"}
            new_value = {'$inc': {'donutCounter': 1}}
            collection.update_one(query, new_value)
            x = collection.find({'id': message.author.id})
            await message.channel.send(f'```Thank you for informing me that you are a failure.```')
        # end section

        # this code allows the user to add themselves to the database
        if message.content.startswith('.add me') and message.content.endswith('.add me'):
            query = {'id': f"{message.author.id}"}
            d = collection.find_one(query)
            if d:
                await message.channel.send("you are already registered in the database.")
            else:
                entry = {"id": f"{message.author.id}", "username": f"{message.author}", "donutCounter": 0,
                         "bitchCounter": 0, "aceCounter": 0, "teamkillCounter": 0, "teamkilled": "None"}
                collection.insert_one(entry)
                await message.channel.send(f"you have been added to the database of donuts.")
        elif message.content.startswith('.add') and not message.content.endswith('.add me'):
            await message.channel.send(f'```Users cannot add other users to the database, only the admin or the user '
                                       f'himself can.```')
        # end section

        # this section of code lets players log themselves and log other players info
        if message.content.startswith('.log') and message.content.endswith('.log'):
            query = {'id': f"{message.author.id}"}
            d = collection.find_one(query)
            sub_start = "{'_id'"
            sub_end = "'user"
            f = re.sub(r'{}.*?{}'.format(re.escape(sub_start), re.escape(sub_end)), '', str(d))
            x = f.replace("'", "")
            g = x.replace(",", "\n")
            n = g.replace("}", "")
            await message.channel.send(f"```{n}```")

        if message.content.startswith('.show') and message.content.endswith('log'):
            query = {'id': f"{message.mentions[0].id}"}
            d = collection.find_one(query)
            sub_start = "{'_id'"
            sub_end = "'user"
            f = re.sub(r'{}.*?{}'.format(re.escape(sub_start), re.escape(sub_end)), '', str(d))
            x = f.replace("'", "")
            g = x.replace(",", "\n")
            n = g.replace("}", "")
            await message.channel.send(f"```{n}```")
        # end section

        if message.content.startswith('.help'):
            await message.channel.send('```1. To add yourself to the database use ".add me"\n'
                                       '2. To add a donut to your counter use the command ".i suck"\n'
                                       '3. To report someone for being a bitch use command ".<tag user> is a bitch"\n'
                                       '4. To report a teamkill use the command ".teamkill <tag user that teamkilled> '
                                       '<tag user that got killed>"\n'
                                       '5. To add an ACE to a users counter use the command ". <tag user that has '
                                       'aced> got an ace"\n'
                                       '6. To view your counter use the command ".log"\n'
                                       '7. To view another users logs use the command ".show <tag user> log"\n'
                                       'NOTE : all commands are lowercase!```')
        await bot.process_commands(message)

    @bot.command()
    async def help_me(ctx):
        await ctx.send('```1. To add yourself to the database use "?add_me"\n'
                       '2. To add a DONUT to your counter use the command "?donut"\n'
                       '3. To report someone for being a BITCH use command "?bitch <tag user>"\n'
                       '4. To report a TEAMKILL use the command "?teamkill <tag user that teamkilled> '
                       '<tag user that got killed>"\n'
                       '5. To add an ACE to a users counter use the command "?ace <tag user that has '
                       'aced>"\n'
                       '6. To VIEW YOUR COUNTER use the command "?log"\n'
                       '7. To VIEW ANOTHER USERS LOGS use the command "?show <tag user>"\n'
                       '8. To add a CARRY to a user use the command "?carry <tag user>"\n'
                       'NOTE : all commands are lowercase!```')

    @bot.command()
    async def play(ctx):
        voice_user = ctx.message.author.voice
        music_client = await voice_user.channel.connect(cls=MusicClient)
        track = Track(
            WAVAudio('media/audio1.wav'),  # AudioSource
            'This is audio'  # name
        )
        await music_client.play(track)

    @bot.command()
    async def donut(ctx):
        query = {'id': f"{ctx.author.id}"}
        new_value = {'$inc': {'donutCounter': 1}}
        collection.update_one(query, new_value)
        x = collection.find({'id': ctx.author.id})
        await ctx.send(f'```Thank you for informing me that you are a failure.```')

    @bot.command()
    async def bitch(ctx, member: discord.Member):
        try:
            if member:
                query = {'id': f"{ctx.message.mentions[0].id}"}
                f = collection.find_one(query)
                if f:
                    new_value = {'$inc': {'bitchCounter': 1}}
                    collection.update_one(query, new_value)
                    x = collection.find({'id': ctx.message.author.id})
                    await ctx.send(f'```{ctx.message.mentions[0]} Has been called out for being a BITCH!```')
                else:
                    await ctx.send(f'```This user has not yet been added to the database.```')
            else:
                await ctx.send("```You didn't tag a user. \nThe correct command is: ?bitch <@User>.```")
        except discord.ext.commands.errors.CommandNotFound:
            await ctx.send("```Your command is not right! refer to ?help_me.```")

    @bot.command()
    async def ace(ctx, user: discord.Member):
        if user:
            if ctx.author.id != ctx.message.mentions[0].id:
                query = {'id': f'{ctx.message.mentions[0].id}'}
                f = collection.find_one(query)
                if f:
                    new_value = {'$inc': {'aceCounter': 1}}
                    collection.update_one(query, new_value)
                    await ctx.send(f'```{ctx.message.mentions[0]} has aced!!```')
                else:
                    await ctx.send('```User does not exist in database.```')
            else:
                await ctx.send('```A user is not allowed to give themself an ace counter.```')
        else:
            await ctx.send("```You have to tag a user after ?ace```")

    @bot.command()
    async def teamkill(ctx, teamkiller: discord.Member, teamkilled: discord.Member):
        if teamkiller and teamkilled:
            query = {'id': f"{ctx.message.mentions[0].id}"}
            f = collection.find_one(query)
            if f:
                new_value = {'$inc': {'teamkillCounter': 1}}
                new_value2 = {'$set': {'teamkilled': f'{ctx.message.mentions[1]}'}}
                collection.update_one(query, new_value)
                collection.update_one(query, new_value2)
                await ctx.send(f'```{ctx.message.mentions[0]} has just teamkilled {ctx.message.mentions[1]}.```')
            else:
                await ctx.send(f'```There is something wrong with your command!```')
        else:
            await ctx.send("```Your message does not contain the necessary tags => ?help_me```")

    @bot.command()
    async def carry(ctx, carrier: discord.Member):
        if carrier:
            query = {'id': f'{ctx.message.mentions[0].id}'}
            f = collection.find_one(query)
            if f:
                new_value = {'$inc': {'carryCounter': 1}}
                collection.update_one(query, new_value)
                await ctx.send(f'```{ctx.message.mentions[0]} has carried!```')
            else:
                await ctx.send(f'```Tagged user could not be found in database!```')
        else:
            await ctx.send(f'```No user has been tagged => "?carry <tag user>".')

    @bot.command()
    async def add_me(ctx):
        query = {'id': f"{ctx.author.id}"}
        d = collection.find_one(query)
        if d:
            await ctx.send("```you are already registered in the database.```")
        else:
            entry = {"id": f"{ctx.author.id}", "username": f"{ctx.author}", "donutCounter": 0,
                     "bitchCounter": 0, "carryCounter": 0, "aceCounter": 0, "teamkillCounter": 0, "teamkilled": "None"}
            collection.insert_one(entry)
            await ctx.send("```you have been added to the database!```")

    @bot.command()
    async def add_user(ctx):
        if ctx.author.id == 308367178715889664:
            if ctx.message.mentions:
                query = {'id': f"{ctx.message.mentions[0].id}"}
                d = collection.find_one(query)
                if d:
                    await ctx.send("```user already registered in the database.```")
                else:
                    entry = {"id": f"{ctx.message.mentions[0].id}", "username": f"{ctx.message.mentions[0]}",
                             "donutCounter": 0,
                             "bitchCounter": 0, "carryCounter": 0, "aceCounter": 0, "teamkillCounter": 0,
                             "teamkilled": "None", "guildId": f"{ctx.guild.id}"}
                    collection.insert_one(entry)
                    await ctx.send("```user added to the database!```")
            else:
                await ctx.send("```You have to tag a user after the command!")

    @bot.command()
    async def show(ctx, member: discord.Member):
        if member:
            query = {'id': f"{ctx.message.mentions[0].id}"}
            d = collection.find_one(query)
            sub_start = "{'_id'"
            sub_end = "'user"
            f = re.sub(r'{}.*?{}'.format(re.escape(sub_start), re.escape(sub_end)), '', str(d))
            x = f.replace("'", "")
            g = x.replace(",", "\n")
            n = g.replace("}", "")
            await ctx.send(f"```{n}```")
        else:
            await ctx.send(f"```You must mention another user!```")

    @bot.command()
    async def log(ctx):
        query = {'id': f"{ctx.author.id}"}
        d = collection.find_one(query)
        sub_start = "{'_id'"
        sub_end = "'user"
        f = re.sub(r'{}.*?{}'.format(re.escape(sub_start), re.escape(sub_end)), '', str(d))
        x = f.replace("'", "")
        g = x.replace(",", "\n")
        n = g.replace("}", "")
        await ctx.send(f"```{n}```")

    @bot.command()
    async def retract(ctx, amount: int, entry: str):
        if ctx.author.id == 308367178715889664:
            if ctx.message.mentions:
                if amount:
                    if entry:
                        query = {'id': f"{ctx.message.mentions[0].id}"}
                        d = collection.find_one(query)
                        if d:
                            new_value = {'$inc': {f"{entry}": -amount}}
                            collection.update_one(query, new_value)
                            await ctx.send(
                                f"```The {entry} for {ctx.message.mentions[0]} has been decreased by -{amount}!```")
                        else:
                            await ctx.send(f"```user does not exist in database```")
                    else:
                        await ctx.send(f"```You have to provide a field to update```")
                else:
                    await ctx.send(f"```you have to give the amount to decrease from the given field```")
            else:
                await ctx.send(f"```no user has been mentioned```")
        else:
            await ctx.send(f"```only the admin can decrease values```")

    @bot.command()
    async def results(ctx):
        result = collection.aggregate([
            {'$match': {"guildId": f"{ctx.guild.id}"}},
            {
                '$addFields': {
                    'finalpoints': {
                        '$subtract': [
                            {
                                '$sum': [
                                    {
                                        '$multiply': [
                                            '$bitchCounter', 2
                                        ]
                                    }, {
                                        '$multiply': [
                                            '$donutCounter', 10
                                        ]
                                    }, {
                                        '$multiply': [
                                            '$teamkillCounter', 15
                                        ]
                                    }
                                ]
                            },
                            {
                                '$sum': [
                                    {
                                        '$multiply': [
                                            '$aceCounter', 10
                                        ]
                                    }, {
                                        '$multiply': [
                                            '$carryCounter', 2
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }, {
                '$sort': {
                    'finalpoints': -1
                }
            }
        ])
        for document in result:
            l = document
            sub_start = "{'_id'"
            sub_end = "'user"
            f = re.sub(r'{}.*?{}'.format(re.escape(sub_start), re.escape(sub_end)), '', str(l))
            sub_start2 = "donut"
            sub_end2 = "final"
            s = re.sub(r'{}.*?{}'.format(re.escape(sub_start2), re.escape(sub_end2)), '', str(f))
            x = s.replace("'", "")
            g = x.replace(",", "\n")
            n = g.replace("}", "")
            await ctx.send(f"```{n}```")

    @bot.command()
    async def ai(ctx, *, message):
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=message,
            temperature=0.7,
            max_tokens=500,
            n=1,
            stop=None,
            timeout=15
        )

        await ctx.send(response.choices[0].text.strip())

    bot.run(TOKEN)
