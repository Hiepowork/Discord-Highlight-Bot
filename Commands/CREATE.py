import os
import discord
from Commands import UTILS
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

async def stitch_and_save_videos(videoPath, choices):
    clips = [VideoFileClip(path) for path in choices]
    final_clip = concatenate_videoclips(clips)
    output_path = os.path.join(videoPath, 'montage.mp4')
    os.makedirs(videoPath, exist_ok=True)
    final_clip.write_videofile(output_path)
    return output_path

async def create_random_montage(message, member_id, amount):
    path = f'downloads/{member_id}'
    files = UTILS.get_all_file_paths(path)
    if (len(files) == 1):
        await message.channel.send("Not enough videos to make a montage")
        return
    
    if len(files) < amount:
        amount = len(files)
    choices = random.sample(files, amount)
    videoPath = f'temp/{member_id}'
    file = await stitch_and_save_videos(videoPath, choices)
    discordFile = discord.File(file)
    await message.channel.send(file = discordFile)
    await message.channel.send("Hey <@" + str(member_id) + "> here's the montage you requested!!!")
    #os.remove(file)

async def create_playlist_montage(message, playlist, member_id, amount):
    path = f'downloads/{member_id}/{playlist}'
    files = UTILS.get_all_file_paths(path)
    if (len(files) == 1):
        await message.channel.send("Not enough videos to make a montage")
        return
    
    if len(files) < amount:
        amount = len(files)
    choices = random.sample(files, amount)
    videoPath = f'temp/{member_id}'
    file = await stitch_and_save_videos(videoPath, choices)
    discordFile = discord.File(file)
    await message.channel.send(file = discordFile)
    await message.channel.send("Hey <@" + member_id + "> here's the montage you requested!!!")
    #os.remove(file)

async def handle_create_message(message):
    content = await UTILS.messageHandler(message)
    playlist = content[1]
    member_id = message.author.id
    amount = 5
    if (playlist == "RANDOM"):
        await create_random_montage(message, member_id, amount)
    else:
        if (playlist.isdigit()):
            playlist = await UTILS.findPlaylistByNumber(playlist, member_id)
        await create_playlist_montage(message, playlist, member_id, amount)
        