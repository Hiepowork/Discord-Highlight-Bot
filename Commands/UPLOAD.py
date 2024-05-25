import os
import aiohttp
from Commands import UTILS
import subprocess

async def getLastFileIndex(existing_files):
    highest_index = -1
    for filename in existing_files:
        if filename.endswith('.mp4'):
            try:
                index = int(filename.split('-')[0])
                if index > highest_index:
                        highest_index = index
            except ValueError:
                pass  # Ignore filenames that don't follow the expected format
    return highest_index + 1
async def compress_video(input_file, output_file, crf=28, preset="medium"):
    """
    Compress an MP4 video file using FFmpeg with a maximum resolution of 900p and a maximum frame rate of 30 fps.

    :param input_file: Path to the input video file.
    :param output_file: Path to the output (compressed) video file.
    :param crf: Constant Rate Factor (lower values mean better quality and larger file size).
    :param preset: Preset for compression speed vs. compression ratio.
    """
    command = [
        'ffmpeg', 
        '-i', input_file,  # Input file
        '-vf', 'scale=1600:900:force_original_aspect_ratio=decrease',  # Video filter for scaling
        '-r', '30',  # Frame rate
        '-vcodec', 'libx264',  # Video codec
        '-crf', str(crf),  # Constant Rate Factor
        '-preset', preset,  # Preset
        output_file  # Output file
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Video compressed successfully and saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        raise

async def download_attachment(message, attachment, member_id, playlist, title):
    if not attachment.filename.lower().endswith('.mp4'):
        await message.channel.send("File must be an MP4")
        return
    
    temp_path = f'temp/{member_id}/{playlist}'
    output_path = f'downloads/{member_id}/{playlist}'
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    existing_files = os.listdir(output_path)
    file_name = f"{await getLastFileIndex(existing_files)}-{title}.mp4"
    temp_file_path = os.path.join(temp_path, file_name)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status == 200:
                    with open(temp_file_path, 'wb') as f:
                        f.write(await resp.read())
                    print(f'Downloaded {attachment.filename} to {temp_file_path}')
                else:
                    print(f'Failed to download {attachment.filename}')
                    return
        
        # Compress the downloaded file
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        output_file_path = os.path.join(output_path, file_name)
        await compress_video(temp_file_path, output_file_path)
        
        # Remove the temporary file
        os.remove(temp_file_path)
        print(f"Temporary file {temp_file_path} removed")
        
        # Remove the temporary directory if empty
        if not os.listdir(temp_path):
            os.rmdir(temp_path)
            print(f"Temporary directory {temp_path} removed")
        
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        # Cleanup in case of any error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary file {temp_file_path} removed due to error")
        if os.path.exists(temp_path) and not os.listdir(temp_path):
            os.rmdir(temp_path)
            print(f"Temporary directory {temp_path} removed due to error")
async def handle_upload_message(message):
    
    content = await UTILS.messageHandler(message)
    playlist = content[1]
    member_id = message.author.id
    title = content[2] 
    if message.attachments and len(message.attachments) == 1:
        if len(message.attachments) == 1:
            await download_attachment(message, message.attachments[0], member_id, playlist, title)
        else:
            await message.channel.send("One file at a time!")
            return
    else:
        await message.channel.send("No attachment given")
        return