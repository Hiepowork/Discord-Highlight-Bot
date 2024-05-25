import discord
import os
async def checkMemberIdValid(message, member_id):
    if (member_id.isdigit()):
        guild_member = discord.utils.get(message.guild.members, id=int(member_id))
        if (guild_member == None):
            await message.channel.send("Wrong format")
            return None
    else:
        await message.channel.send("Wrong format")
        return None
    return member_id

def parse_command(content):
    in_quote = False
    current_quote = ""
    returner = []
    
    i = 0
    while i < len(content):
        char = content[i]
        
        if char == '"':
            if in_quote:
                # Ending a quoted string
                in_quote = False
                returner.append(f'"{current_quote.strip()}"')
                current_quote = ""
            else:
                # Starting a quoted string
                in_quote = True
            i += 1
        elif char == ' ' and not in_quote:
            i += 1
        else:
            if in_quote:
                current_quote += char
            else:
                current_word = ""
                while i < len(content) and content[i] not in [' ', '"']:
                    current_word += content[i]
                    i += 1
                
                # Process potential user ID
                if current_word.startswith("<@") and current_word.endswith(">"):
                    current_word = current_word[2:-1]
                
                returner.append(current_word)
                continue
            i += 1
    
    # Handle case where input ends while still in quotes
    if current_quote:
        returner.append(f'"{current_quote.strip()}"')
    
    return returner

async def removeQuotes(content):
    if content[0] == '"' and content[-1] == '"':
        content = content[1:len(content) - 1]
    return content

async def messageHandler(message):
    content = parse_command(message.content)
    
    if (message.content.startswith("!UPLOAD")):
        if (len(content) != 2 and len(content) != 3):
            return None
        if(len(content) == 2):
            content[1] = await removeQuotes(content[1])
            content.append("Untitled")
        else:
            content[1] = await removeQuotes(content[1])
            content[2] = await removeQuotes(content[2])
        return content
    
    elif (message.content.startswith("!LIST")):
        if (len(content) != 2 and len(content) != 3):
            return None
        content[1] = await removeQuotes(content[1])
        return content
    
    elif(message.content.startswith("!REMOVE")):
        if len(content) != 2 and len(content) != 3:
            return None
        content[1] = await removeQuotes(content[1])
        return content
    
    elif(message.content.startswith("!RENAME")):
        if len(content) != 3 and len(content) != 4:
            return None
        if len(content) == 3:
            content.append(None)
        content[1] = await removeQuotes(content[1])
        content[2] = await removeQuotes(content[2])
        return content
        
    elif(message.content.startswith("!SHOW")):
        if len(content) != 2 and len(content) != 3:
            return None
        content[1] = await removeQuotes(content[1])
        return content
    
    elif(message.content.startswith("!RANDOM")):
        if len(content) != 1:
            return None
        return content
    
    elif(message.content.startswith("!CREATE")):
        if len(content) != 3:
            return None
        content[1] = await removeQuotes(content[1])
        return content
    elif(message.content.startswith("!HELP")):
        if len(content) != 1:
            return None
        return content
    
async def findPlaylistByNumber(number, member_id):
    path = f'downloads/{member_id}'
    if not os.path.exists(path):
        return number
    existing_directories = os.listdir(path)
    if int(number) >= len(existing_directories):
        return number
    return existing_directories[int(number)]

def get_all_file_paths(directory):
    """
    Get a list of all file paths in the specified directory and its subdirectories.

    :param directory: str, path to the directory
    :return: list of str, paths to all files in the directory
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths