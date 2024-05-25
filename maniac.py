import discord
import os
from dotenv import load_dotenv
import sys
sys.path.append('/Commands')
import random

from Commands import UPLOAD
from Commands import LIST
from Commands import REMOVE
from Commands import RENAME
from Commands import SHOW
from Commands import CREATE
from Commands import UTILS

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = discord.Client(intents=intents)

    
    @client.event
    async def on_ready():
        print(f'{client.user} is now online!')
    
    async def alertUsers(message):
        content = message.content.split()
        names = ""
        for k in range (1, len(content) - 1):
            names += content[k] + " " 
        amount = int(content[-1])
        if (amount > 25):
            amount = 25
            await message.channel.send("Number of alerts too high, set to 25")
        for i in range (0, amount):
            await message.channel.send(names)
    async def handle_help_message(message):
        help_message = """
        !UPLOAD `"[name of playlist]"` `"[title of video]"` - video will be untitled
    
        !LIST PLAYLISTS `[optional page number]`
        !LIST `"[name of playlist]"` `[optional page number]`
        !LIST `[playlist number]` `[optional page number]`
    
        !REMOVE `"[name of playlist]"`
        !REMOVE `"[name of playlist]"` `[id of video]`
    
        !RENAME `"[name of playlist]"` `"[new playlist title]"`
        !RENAME `"[name of playlist]"` `"[new video title]"` `[id of video]`
        !RENAME `[playlist number]` `"[new playlist title]"`
        !RENAME `[playlist number]` `"[new video title]"` `[id of video]`
    
        !SHOW `"[name of playlist]"`
        !SHOW `"[name of playlist]"` `[id of video]`
        !SHOW `[playlist number]`
        !SHOW `[playlist number]` `[id of video]`
        !RANDOM 
    
        !CREATE RANDOM MONTAGE
        !CREATE `[playlist number]` MONTAGE
        !CREATE `"[name of playlist]"` MONTAGE
        """
        await message.channel.send(help_message)
    @client.event
    async def on_message(message):
        content = message.content
        if (content.startswith("!HELP")):
            await handle_help_message(message)
            return
        elif (content.startswith("!UPLOAD")):
            await UPLOAD.handle_upload_message(message)
            return
        elif (content.startswith("!LIST")):
            await LIST.handle_list_message(message)
            return
        elif (content.startswith("!RENAME")):
            await RENAME.handle_rename_message(message)
            return
        elif (content.startswith("!REMOVE")):
            await REMOVE.handle_remove_message(message)
            return
        elif (content.startswith("!SHOW")):
            await SHOW.handle_show_message(message)
            return
        elif (content.startswith("!RANDOM")):
            await SHOW.handle_random_message(message)
            return
        elif (content.startswith("!CREATE")):
            await CREATE.handle_create_message(message)
            return


        if(content.startswith("!ALERT")):
            await alertUsers(message)
        elif (content.startswith("!RankedOrUnrated")):
            await message.channel.send("The oracle says... " + random.choice(['Unrated', 'Ranked']) + "!!!")
    client.run(TOKEN)