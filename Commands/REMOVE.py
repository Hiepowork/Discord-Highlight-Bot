import os
from Commands import UTILS

async def remove_playlist(message, playlist, member_id):
    path = f'downloads/{member_id}/{playlist}'
    if not os.path.exists(path):
        await message.channel.send(f"No playlist called {playlist} found for user <@{member_id}>")
        return
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(path)
    await message.channel.send(f"PLAYLIST {playlist} removed")

async def remove_video(message, playlist, member_id, file_id):
    path = f'downloads//{member_id}/{playlist}'
    if not os.path.exists(path):
        await message.channel.send(f"No playlist {playlist} found for <@{member_id}>")
        return

    existing_files = os.listdir(path)
    file_to_remove = None
    for file in existing_files:
        if file.split('-')[0] == file_id:
            file_to_remove = file
            break

    if file_to_remove:
        os.remove(os.path.join(path, file_to_remove))
        await message.channel.send(f"File {file_to_remove.split('-')[1]} removed")
        if len(existing_files) == 1:
            await remove_playlist(message, playlist, member_id)
    else:
        await message.channel.send(f"No file with ID {file_id} found")


async def handle_remove_message(message):
    content = await UTILS.messageHandler(message)
    playlist = content[1]
    member_id = message.author.id
    if playlist.isdigit():
        playlist = await UTILS.findPlaylistByNumber(playlist, member_id)
    if (len(content) == 2):
        await remove_playlist(message, playlist, member_id)
    elif (len(content) == 3):
        await remove_video(message, playlist, member_id, content[2])