import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, channel
import pymongo
from discord.ext.commands import bot
from pymongo import MongoClient
from urllib.parse import quote_plus
import re
import config

username = config.username
password = config.password
url = "mongodb+srv://<username>:<password>@discordbot.gltp06j.mongodb.net/?retryWrites=true&w=majority"

url = url.replace("<username>", username).replace("<password>", password)
# encoded_url = quote_plus(url)
pymongoClient = pymongo.MongoClient(url)

db = pymongoClient["DiscordBotDB"]
print('connection has been made to {collection}', db)
collection = db["Donut"]


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = config.tokenkey
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        await client.change_presence(activity=discord.Game('.help | bishes'))

    @client.event
    async def on_message(message):
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
                         "bitchCounter": 0, "aceCounter": 0, "teamkillCounter": 0}
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
            await message.channel.send(f"```here is your database info => {x}```")

        if message.content.startswith('.show') and message.content.endswith('log'):
            query = {'id': f"{message.mentions[0].id}"}
            d = collection.find_one(query)
            sub_start = "{'_id'"
            sub_end = "'user"
            f = re.sub(r'{}.*?{}'.format(re.escape(sub_start), re.escape(sub_end)), '', str(d))
            x = f.replace("'", "")
            await message.channel.send(f"```here is the database info of {message.mentions[0]} => {x}```")
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

    client.run(TOKEN)
