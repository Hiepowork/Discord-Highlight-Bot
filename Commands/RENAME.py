import os
from Commands import UTILS

async def change_playlist_name(message, playlist, member_id, new_title):
    path = f'downloads/{member_id}/{playlist}'
    new_path = f'downloads/{member_id}/{new_title}'
    
    if not os.path.exists(path):
        await message.channel.send(f"No playlist called {playlist} found for user <@{member_id}>")
        return

    if os.path.exists(new_path):
        await message.channel.send(f"A playlist with the name {new_title} already exists for user <@{member_id}>")
        return
    
    os.rename(path, new_path)
    await message.channel.send(f"Playlist {playlist} renamed to {new_title}")

async def change_video_name(message, playlist, member_id, new_title, file_id):
    path = f'downloads/{member_id}/{playlist}'
    if not os.path.exists(path):
        await message.channel.send(f"No playlist called {playlist} found for user <@{member_id}>")
        return
    
    existing_files = os.listdir(path)
    file_to_rename = None
    for file in existing_files:
        if file.split('-')[0].strip() == file_id.strip():
            file_to_rename = file
            break
    if file_to_rename:
        new_file_name = f"{file_id}-{new_title}.mp4"
        os.rename(os.path.join(path, file_to_rename), os.path.join(path, new_file_name))
        await message.channel.send(f"File {file_to_rename} renamed to {new_file_name}")
    else:
        await message.channel.send(f"No file with ID {file_id} found")


async def handle_rename_message(message):
    content = await UTILS.messageHandler(message)
    playlist = content[1]
    title = content[2]
    member_id = message.author.id
    if (playlist.isdigit()):
        playlist = await UTILS.findPlaylistByNumber(playlist, member_id)
    if (content[3] == None):
        #Change playlist name
        await change_playlist_name(message, playlist, member_id, title)
    else:
        #Change video name
        await change_video_name(message, playlist, member_id, title, content[3])