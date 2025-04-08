print("\n Initialising bot.py")
# The core bot, focusing on interacting with Discord and being the interactable interface

import discord
import datetime
import tomb_project
import re
import traceback

# A function to clean the user response for input commands
def clean_response(raw_user_message) -> str:    
    clean = raw_user_message.lower()
    clean = re.sub('[^A-Za-z0-9 ]+', '', clean)
    while clean[0] == ' ':
        clean = clean[1:]
    return clean

# The way the bot sends messages to users
async def send_message(message):
    # Check if message is private or public
    is_private = isinstance(message.channel, discord.DMChannel)

    # If it is a valid message, refer to server.enact_response for next action
    if (is_private or message.content.startswith('|')) and (len(message.content) < 60):
        clean_message = clean_response(message.content)
        try:
            # Download all game session data into object game_session_temp for the messaging user            
            game_session_temp = tomb_project.game_session(message.author.name, *tomb_project.download_database(message.author.name))

            # Modify game_session_temp with server.enact_response to change gamestate and override game_session_temp
            game_session_temp = tomb_project.handle_input(game_session_temp, message, clean_message)

            # print(type(game_session_temp))
            # Use new game_session_temp to output game action response (or error)
            response = game_session_temp.find_output()

            # Update all new changes to MongoDB via game_session procedure
            print(f"\n============================================\ntombproject -> {response}\n============================================\n")
            if is_private:
                await message.author.send(response)
            else:
                await message.channel.send(response)

            # Once everything is completed, upload any changes to the database
            tomb_project.upload_to_database(game_session_temp)

        except Exception:
            traceback.print_exc()
        
def run_bot():
    token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    # Startup event handler
    @client.event
    async def on_ready():
        for guild in client.guilds:
            default_channel = guild.system_channel
            if default_channel:
                current_datetime = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
                await default_channel.send("TombProject has activated at {current_datetime}!".format(current_datetime=current_datetime))
            else:
                print(f"Unable to send message in guild '{guild.name}' - no default channel found.")

        print(f'{client.user} is now running!')
        
    # User message event handler
    @client.event
    async def on_message(message):
        # If bot sent the message or the message is empty, ignore
        if message.author == client.user:
            return
        
        # Otherwise, consult the send_message function
        await send_message(message)
            
    client.run(token)
