import discord
from discord.ext import commands
import pymongo
import re
import config
import asyncio
from urllib import parse, request
import json
import random
import requests

# api gify
url = "http://api.giphy.com/v1/gifs/search"
lastCommandAuthor = ""
fullmessage = ""
lastCommandContent = None
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
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        await bot.change_presence(activity=discord.Game('?help | bishes'))

    @bot.event
    async def on_message(message):
        if not message.content.startswith('?reverse'):
            global lastCommandContent
            lastCommandContent = message.content
            lastCommandAuthor = message.author.id
            print(lastCommandContent)
        await bot.process_commands(message)
    
    @bot.command()
    async def reverse(ctx):
        print(lastCommandContent)
        if lastCommandContent.startswith('?bitch '):
            query = {'id': f"{lastCommandAuthor}"}
            f = collection.find_one(query)
            if f:
                new_value = {'$inc': {'bitchCounter': 2}}
                collection.update_one(query, new_value)
                x = collection.find({'id': ctx.message.author.id})
                embed = discord.Embed(title=f'{lastCommandAuthor} has been called out for wrongfully giving a bitchCounter and reveices 2 bitchCounters!', color=0xffd700)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'```This user has not yet been added to the database.```')
        else:
            await ctx.send("```You didn't tag a user. \nThe correct command is: ?bitch <@User>.```")

    @bot.command()
    async def triple0(ctx, member:discord.Member):
        try:
            if member:
                query = {'id': f"{ctx.message.mentions[0].id}"}
                f = collection.find_one(query)
                if f:
                    new_value = {'$inc': {'triple0': 1}}
                    collection.update_one(query, new_value)
                    x = collection.find({'id': ctx.message.author.id})
                    embed = discord.Embed(title=f'{ctx.message.mentions[0]} has done a TRIPLE0!', color=0xffd700)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='Command has failed!', color=0xffd700)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='NO user has been tagged!', color=0xffd700)
                await ctx.send(embed=embed)
        except discord.ext.commands.errors.CommandNotFound:
            await ctx.send("```Your command is not right! refer to ?help_me.```")

    @bot.command()
    async def help(ctx):
        embed = discord.Embed(title="Commands",description="These are the commands for the bot:",color=0xffffff)
        embed.add_field(name="Adding to database",value="To add yourself to the database, type '?add_me'")
        embed.add_field(name="Bitch", value="To declare someone a bitch, type '?bitch <tag user>'")
        embed.add_field(name="Donut", value="if you achieved a donut, type '?donut'")
        embed.add_field(name="Teamkill", value="To report a teamkill, type '?teamkill <user THAT teamkilled> <user that GOT teamkilled>'")
        embed.add_field(name="Ace", value="To award an ace to a player, type '?ace <tag user>'")
        embed.add_field(name="Carry", value="To add a carry counter, type '?carry <tag user>'")
        embed.add_field(name="Log", value="To view your log use the command '?log'")
        embed.add_field(name="Show", value="To view another users logs, type '?show <tag user>'")
        embed.add_field(name="triple0", value="To grant a triple0, type '?triple0 <tag user>'")
        embed.add_field(name="Scoreboard", value="To view the scoreboard type '?results'")
        embed.set_footer(text="All commands are LOWERCASE")
        embed.set_thumbnail(url="https://natashaskitchen.com/wp-content/uploads/2021/05/Glazed-Donuts-SQ.jpg")
        embed.set_author(name="DonutBot", icon_url="https://natashaskitchen.com/wp-content/uploads/2021/05/Glazed-Donuts-SQ.jpg")
        await ctx.send(embed=embed)

    @bot.command()
    async def donut(ctx):
        randomNumb = random.randint(1, 14)

        query = {'id': f"{ctx.author.id}"}
        new_value = {'$inc': {'donutCounter': 1}}
        collection.update_one(query, new_value)
        x = collection.find({'id': ctx.author.id})

        if randomNumb == 1:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=ass&limit=1'
        elif randomNumb == 2:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=you-are-a-bitch&limit=1'
        elif randomNumb == 3:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=you-suck&limit=1'
        elif randomNumb == 4:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=poop&limit=1'
        elif randomNumb == 5:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=I-am-blind&limit=1'
        elif randomNumb == 6:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=homer-simpson-donut&limit=1'
        elif randomNumb == 7:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=emotional-damage&limit=1'
        elif randomNumb == 8:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=loser&limit=1'
        elif randomNumb == 9:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=hiding&limit=1'
        elif randomNumb == 10:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=i-hope-nobody-saw-that&limit=1'
        elif randomNumb == 11:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=donut&limit=1'
        elif randomNumb == 12:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=useless&limit=1'
        elif randomNumb == 13:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=pathetic&limit=1'
        elif randomNumb == 14:
            url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=failure&limit=1'

        response = requests.get(url)
        data = json.loads(response.text)

        if len(data['data']) > 0:
            gif_url = data['data'][0]['images']['fixed_height']['url']
        else:
            await ctx.send("No GIFs were found!")
        embed = discord.Embed(title=f'{ctx.author} has received a donut!', color=0xffd700)
        embed.set_image(url=gif_url)

        await ctx.send(embed=embed)

    @bot.command()
    async def givedonut(ctx, member: discord.Member):
        try:
            if member:
                query = {'id': f"{ctx.message.mentions[0].id}"}
                f = collection.find_one(query)
                if f:
                    new_value = {'$inc': {'donutCounter': 1}}
                    collection.update_one(query, new_value)
                    x = collection.find({'id': ctx.message.mentions[0].id})
                    await ctx.send(
                        f'```{ctx.message.mentions[0]} has received a donutCounter from {ctx.message.author}!```')
                else:
                    await ctx.send(f'```This user has not yet been added to the database.```')
            else:
                await ctx.send("```You didn't tag a user. \nThe correct command is: ?bitch <@User>.```")
        except discord.ext.commands.errors.CommandNotFound:
            await ctx.send("```Your command is not right! refer to ?help_me.```")

    @bot.command()
    async def bitch(ctx, member: discord.Member):
        randomNumb = random.randint(1, 4)
        try:
            if member:
                query = {'id': f"{ctx.message.mentions[0].id}"}
                f = collection.find_one(query)
                if f:
                    new_value = {'$inc': {'bitchCounter': 1}}
                    collection.update_one(query, new_value)
                    x = collection.find({'id': ctx.message.author.id})
                    

                    if randomNumb == 1:
                        url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=dumbass-bitch&limit=1'
                    elif randomNumb == 2:
                        url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=behave-yourself&limit=1'
                    elif randomNumb == 3:
                        url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=bitchy&limit=1'
                    elif randomNumb == 4:
                        url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=cunt&limit=1'

                    response = requests.get(url)
                    data = json.loads(response.text)

                    if len(data['data']) > 0:
                        gif_url = data['data'][0]['images']['fixed_height']['url']
                    else:
                        await ctx.send("No GIFs were found!")
                    embed = discord.Embed(title=f'{ctx.message.mentions[0]} has been called out for being a bitch!', color=0xffd700)
                    embed.set_image(url=gif_url)

                    await ctx.send(embed=embed)

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
                randomNumb = random.randint(1, 9)
                if randomNumb == 1:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=teamkill-slaps&limit=1'
                elif randomNumb == 2:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=teamkill-dissapointment&limit=1'
                elif randomNumb == 3:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=teamkilleveryone&limit=1'
                elif randomNumb == 4:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=poop&limit=1'
                elif randomNumb == 5:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=I-am-blind&limit=1'
                elif randomNumb == 6:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=friendly-fire&limit=1'
                elif randomNumb == 7:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=wtf-bruh&limit=1'
                elif randomNumb == 8:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=falling-down-stairs&limit=1'
                elif randomNumb == 9:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=suicide&limit=1'

                response = requests.get(url)
                data = json.loads(response.text)

                if len(data['data']) > 0:
                    gif_url = data['data'][0]['images']['fixed_height']['url']
                else:
                    await ctx.send("No GIFs were found!")

                new_value = {'$inc': {'teamkillCounter': 1}}
                new_value2 = {'$set': {'teamkilled': f'{ctx.message.mentions[1]}'}}
                collection.update_one(query, new_value)
                collection.update_one(query, new_value2)

                embed = discord.Embed(title=f'{ctx.message.mentions[0]} has teamkilled {ctx.message.mentions[1]}!', color=0xff0000)
                embed.set_image(url=gif_url)

                await ctx.send(embed=embed)
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

                randomNumb = random.randint(1, 5)
                if randomNumb == 1:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=carry&limit=1'
                elif randomNumb == 2:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=heavy-backpack&limit=1'
                elif randomNumb == 3:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=dancing-soldier&limit=1'
                elif randomNumb == 4:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=heavy-load&limit=1'
                elif randomNumb == 5:
                    url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q=resist-weight-of-the-world&limit=1'


                response = requests.get(url)
                data = json.loads(response.text)

                if len(data['data']) > 0:
                    gif_url = data['data'][0]['images']['fixed_height']['url']
                else:
                    await ctx.send("No GIFs were found!")
                embed = discord.Embed(title=f'{ctx.message.mentions[0]} has carried!', color=0xff0000)
                embed.set_image(url=gif_url)

                await ctx.send(embed=embed)
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
                     "bitchCounter": 0, "carryCounter": 0, "aceCounter": 0, "teamkillCounter": 0, "teamkilled": "None","guildId": f"{ctx.guild.id}", "triple0": 0}
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
                             "teamkilled": "None", "guildId": f"{ctx.guild.id}", "triple0": 0}
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
            embed = discord.Embed(title=f'{ctx.message.mentions[0]} logs', color=0x0000ff, description=n)
            await ctx.send(embed=embed)
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
        embed = discord.Embed(title=f'{ctx.author} logs', color=0x0000ff, description=n)
        await ctx.send(embed=embed)

    @bot.command()
    async def slagroom(ctx, amount: int, entry: str, members: commands.Greedy[discord.Member]):
        print(members[0].id)
        print(entry)
        if amount:
            if entry:
                if entry.startswith('bitch'):
                    for member in members:
                        query = {'id': f"{member.id}"}
                        f = collection.find_one(query)
                        if f:
                            new_value = {'$inc': {"bitchCounter": amount}}
                            collection.update_one(query, new_value)
                        else:
                            await ctx.send("User does not exist in database!")
                    embed = discord.Embed(title=f'all the tagged members have received: {amount} bitchCounter', color=0x0000ff)
                    await ctx.send(embed=embed)

                elif entry.startswith('donut'):
                    for member in members:
                        query = {'id': f"{member.id}"}
                        f = collection.find_one(query)
                        if f:
                            new_value = {'$inc': {"donutCounter": amount}}
                            collection.update_one(query, new_value)
                        else:
                            await ctx.send("User does not exist in database!")
                    embed = discord.Embed(title=f'all the tagged members have received: {amount} donutCounter', color=0x0000ff)
                    await ctx.send(embed=embed)

                elif entry.startswith('carry'):
                    for member in members:
                        query = {'id': f"{member.id}"}
                        f = collection.find_one(query)
                        if f:
                            new_value = {'$inc': {"carryCounter": amount}}
                            collection.update_one(query, new_value)
                        else:
                            await ctx.send("User does not exist in database!")
                    embed = discord.Embed(title=f'all the tagged members have received: {amount} carryCounter', color=0x0000ff)
                    await ctx.send(embed=embed)
            else:
                await ctx.send("You have to specify wich counter to add points to!")
        else:
            await ctx.send("you have to give the amount of points to add!")
        

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
        number=0;
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
                                    }, {
                                        '$multiply': [
                                            '$triple0', 50
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
        embed = discord.Embed(title='results', color=0x4b0082)
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
            number+=1
            embed.add_field(name=f'#{number}',value=f'{n}',inline=False)

        await ctx.send(embed=embed)

    @bot.command()
    async def gif(ctx, q):
        url = f'https://api.giphy.com/v1/gifs/search?api_key={config.gifytoken}&q={q}&limit=1'
        response = requests.get(url)
        data = json.loads(response.text)

        if len(data['data']) > 0:
            gif_url = data['data'][0]['images']['fixed_height']['url']
            await ctx.send(gif_url)
        else:
            await ctx.send("No GIFs were found!")

    bot.run(TOKEN)
