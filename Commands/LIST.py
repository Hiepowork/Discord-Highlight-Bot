import os
from dotenv import load_dotenv
from Commands import UTILS

async def list_playlists(message, member_id, page):
    path = f'downloads/{member_id}'
    if not os.path.exists(path):
        await message.channel.send(f"No playlists found for user <@{member_id}>")
        return
    playlist_directories = os.listdir(path)
    starting_index = (int(page) - 1)
    
    addition = 10
    playlist_lists = ""
    if (starting_index + 10) > len(playlist_directories):
        addition = len(playlist_directories) - starting_index

    for i in range (starting_index, starting_index + addition):
        record = str(i) + "\t" + playlist_directories[i] + "\n"
        playlist_lists += record

    playlist_lists += "PAGE " + str(page)
    
    await message.channel.send(f"Playlists for user <@{member_id}>:\n{playlist_lists}")

async def list_playlist(message, playlist, member_id, page):
    path = f'downloads/{member_id}/{playlist}'
    if not os.path.exists(path):
        await message.channel.send(f"No playlist {playlist} found for <@{member_id}>")
        return
    existing_files = os.listdir(path)
    starting_index = (int(page) - 1)
    addition = 10
    file_lists = ""
    if (starting_index + 10) > len(existing_files):
        addition = len(existing_files) - starting_index

    for i in range (starting_index, starting_index + addition):
        file = existing_files[i].split("-")
        record = file[0] + "\t" + file[1] + "\n"
        file_lists += record
    file_lists += "PAGE " + str(page)
    
    await message.channel.send(f"Files in {playlist}:\n{file_lists}")

    
async def handle_list_message(message):
    content = await UTILS.messageHandler(message)
    playlist = content[1]
    member_id = message.author.id
    
    if playlist == "PLAYLISTS":
        if (len(content) == 3):
            page = content[2] 
            await list_playlists(message, member_id, page)
        elif(len(content) == 2):
            await list_playlists(message, member_id, 1)
    else:
        if playlist.isdigit():
            playlist = await UTILS.findPlaylistByNumber(playlist, member_id)
        if (len(content) == 3):
            page = content[2] 
            await list_playlist(message, playlist, member_id, page)
        elif(len(content) == 2):
            await list_playlist(message, playlist, member_id, 1 )