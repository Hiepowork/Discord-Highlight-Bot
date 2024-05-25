import os
import discord
from Commands import UTILS
import random

async def show_playlist_video(message, playlist, member_id):
    path = f'downloads/{member_id}/{playlist}'
    if not os.path.exists(path):
        await message.channel.send(f"No playlist called {playlist} found for user <@{member_id}>")
        return
    
    existing_files = os.listdir(path)
    if (len(existing_files) == 0):
        await message.channel.send(f"No videos in playlist called {playlist} found for user <@{member_id}>")
        return
    file = random.choice(existing_files)
    file_path = path + '/' + file
    with open(file_path, 'rb') as file:
        file = discord.File(file_path)
        await message.channel.send(file = file)
        await message.channel.send("Hey <@" + member_id + "> here's the " + playlist + "you requested!!!\nTITLE: "+ file_path.split('/')[3][2:] + "\nPLAYLIST: "+ file_path.split('/')[2])

async def show_playlist_video_id(message, playlist, member_id, id):
    path = f'downloads/{member_id}/{playlist}'
    if not os.path.exists(path):
        await message.channel.send(f"No playlist called {playlist} found for user <@{member_id}>")
        return
    existing_files = os.listdir(path)
    file_to_find = None
    for file in existing_files:
        if file.split('-')[0].strip() == id:
            file_to_find = file
            break
    if (file_to_find == None):
        await message.channel.send(f"No videos in playlist called {playlist} found for user <@{member_id}> with id {id}")
        return
    file_path = path + '/' + file_to_find
    with open(file_path, 'rb') as file:
        file = discord.File(file_path)
        await message.channel.send(file = file)
        await message.channel.send("Hey <@" + str(member_id) + "> here's the " + playlist + "you requested!!!\nTITLE: "+ file_path.split('/')[3][2:] + "\nPLAYLIST: "+ file_path.split('/')[2])

async def handle_show_message(message):
    content = await UTILS.messageHandler(message)
    playlist = content[1]
    member_id = message.author.id
    if (playlist.isdigit()):
        playlist = await UTILS.findPlaylistByNumber(playlist, member_id)

    if (len(content) == 2):
        await show_playlist_video(message, playlist, member_id)
    elif (len(content) == 3):
        await show_playlist_video_id(message, playlist, member_id, content[2])
        pass

async def handle_random_message(message):
    content = await UTILS.messageHandler(message)
    path = f'downloads/{message.author.id}'
    returned = UTILS.get_all_file_paths(path)
    path = random.choice(returned)
    with open(path, 'rb') as file:
        file = discord.File(path)
        await message.channel.send(file = file)
        await message.channel.send("Hey <@" + str(message.author.id) + "> here's the random video you requested!!!\nTITLE: "+ path.split('-')[1] + "\nPLAYLIST: "+ path.split("\\")[1])