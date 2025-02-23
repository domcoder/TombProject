# tomb_project.py
print("\n Initializing tomb_project.py")
# The logic behind the game, calling modules for data to return to bot.py for responses

# Other modules
import player_character
import dungeon
import item
import text_list
import utilities
import ai_director
import monsters
import combat

# Libraries
import pymongo
from bson import ObjectId
import string
import random
import traceback

# Connect to MongoDB and initialise databases
client = pymongo.MongoClient("mongodb+srv://up2013798:0w8pCszbqwMMFUNO@tombproject.7dxuvmm.mongodb.net/")
db = client["TombProject"]
characters_collection = db["characters"]
rooms_collection = db["dungeon"]
items_collection = db["items"]
director_collection = db["director"]
monsters_collection = db["monsters"]

# Not implemented
# A comprehensive list of most available commands
def _help():
    return "How can I help?"

# Repeats a user's message back to them
def mimic(raw_message):
    mimic_output = raw_message.content[1:].lstrip()
    return mimic_output[6:]

def download_database(player_username):

    # Downloads monsters in dict format
    # For each monster, turn it into an item then convert its weapon and armour into objects
    # Add it to monster_list
    monsters_data = list(monsters_collection.find({}, {"_id": 0}))
    monster_list = []
    for every_monster in monsters_data:
        monster_obj = monsters.Monster(**every_monster)
        monster_list.append(monster_obj)

    if monster_list == []:
        monster_list.append(utilities.return_none_monster(0))

    # Fetch dungeon from the database
    dungeon_data = list(rooms_collection.find({}, {"_id": 0}))
    
    # Check if dungeon_data is empty
    if not dungeon_data:
        dungeon_data = utilities.default_room()
    dungeon_rooms = []

    if isinstance(dungeon_data, dict):
        dungeon_data = [dungeon_data]

    # Iterate over each dictionary in dungeon_data and convert it to a room object
    for room_dict in dungeon_data:
        room_to_add = utilities.dict_to_room(room_dict)
        dungeon_rooms.append(room_to_add)

    # Fill every room object with monster objects
    utilities.populate_dungeon_rooms_with_monsters(dungeon_rooms, monster_list)

    # Fetch items from the database, excluding the _id field
    items_data = list(items_collection.find({}, {"_id": 0}))

    # Check if the items collection is empty
    if len(items_data) < len(utilities.default_items()):
        items_data = utilities.default_items()
    items = [utilities.dict_to_item(every_item) for every_item in items_data]

    # Fetch character from the database
    character_data = characters_collection.find_one({"discord_username": player_username}, {"_id": 0})
        
    # If character not found, create a fresh character
    if not character_data:
        character_data = utilities.default_character(player_username)

    # Load the character object with data from the database
    character = player_character.PlayerCharacter(**character_data)

    # Convert item string names to item objects
    utilities.convert_equipment_name_to_item(character, items)

    # Import the director from the database
    director_data = director_collection.find_one({"director_name": "Director Vulture"}, {"_id": 0, "director_name": 0})
    if not director_data:
        director_data = utilities.default_director()
    director_vulture = ai_director.AiDirector(**director_data)

    # Convert all monster weapons into objects
    for each_monster in monster_list:
        utilities.convert_monster_items_to_item(each_monster, items)

    return character, dungeon_rooms, items, director_vulture, monster_list

def upload_to_database(game_session_instance):
    try:
        if game_session_instance.player_username is not None:
            # Update character data in the database (or add a new one)    
            # First, convert equipped items to their string names
            game_session_instance.character.equipped_weapon = game_session_instance.character.equipped_weapon.item_name
            game_session_instance.character.offhand_item = game_session_instance.character.offhand_item.item_name
            game_session_instance.character.equipped_armour = game_session_instance.character.equipped_armour.item_name
            game_session_instance.character.equipped_talisman = game_session_instance.character.equipped_talisman.item_name
            # The same might need to be done with 'inventory'

            # Next, upload with upsert to correct the database
            characters_collection.update_one({"discord_username": game_session_instance.player_username}, {"$set": game_session_instance.character.to_dict()}, upsert=True)

            # Update dungeon rooms data in the database
            dungeon_rooms = game_session_instance.the_dungeon.return_rooms()
            for room in dungeon_rooms:
                room_dict = room.to_dict()
                room_dict['monster'] = room.monster.name if hasattr(room.monster, 'name') else room.monster
                rooms_collection.update_one({"room_id": room.room_id}, {"$set": room_dict}, upsert=True)

            # Update items data in the database, deleting all old objects
            all_items = game_session_instance.items
            for item_obj in all_items:
                items_collection.update_one({"item_name": item_obj.item_name}, {"$set": item_obj.to_dict()}, upsert=True)

            # Update/upload director
            director_collection.update_one({"director_name": "Director Vulture"}, {"$set": game_session_instance.director.to_dict()}, upsert=True)

            # Upload monsters to the database by first converting their equipment to string names
            all_monsters = game_session_instance.monster_list
            for monster_obj in all_monsters:
                monster_obj.weapon = monster_obj.weapon.item_name
                monster_obj.armour = monster_obj.armour.item_name
                monsters_collection.update_one({"room": monster_obj.room}, {"$set": monster_obj.to_dict()}, upsert=True)

    # Exception to catch upload errors
    except Exception:
        traceback.print_exc()
        print("Upload error.")

class game_session():
    def __init__(self, player_username, character, dungeon_rooms, items, director, monster_list):
        # Identification note
        self.player_username = player_username

        # Situation notes
        self.character = character
        self.the_dungeon = dungeon.Dungeon()
        self.director = director

        # Add rooms to the dungeon
        for room in dungeon_rooms:
            self.the_dungeon.add_room(room)

        self.items = items
        self.monster_list = monster_list

        # The final output text that the bot responds with
        self.output_text = "Handling game related output."

    # A function to return the character via username lookup
    def find_character(self):    
        return self.character

    # Returns the current stored output text
    def find_output(self):
        return self.output_text

    # A function to alter the output text
    def modify_output_text(self, new_text):
        self.output_text = str(new_text)


# An input handler for all game commands
# First it reads the command and chooses an apropriate handling method
# Then it makes any relevant game modifications
# It finally chooses an output message_to_output to send to the user to update them as to what has happened
def handle_input(session, raw_message, command):

    # Print the user's message to the terminal
    print(f'\n============================================\n{raw_message.author.name}: "{command}"\n============================================\n')

    # Default message
    message_to_output = "Sorry, you can't do that."

    # Some miscelaneous functions for testing and general use
    if command == "":
        message_to_output = "..."
    elif command == "hello":
        message_to_output ="Hello!"
    elif command == "roll":
        message_to_output = utilities.funroll()
    elif "mimic" in command:
        message_to_output = mimic(raw_message)
    elif command == "help":
        message_to_output = _help()
    elif command == "test":
        message_to_output = "Test!"

    # A clean-up to ensure no characters are further in the dungeon than exists
    try:
        # Developer commands
        if session.player_username == "mysterycultist":
            if command == "wipe":
                characters_collection.delete_many({})
                rooms_collection.delete_many({})
                items_collection.delete_many({})
                director_collection.delete_many({})
                monsters_collection.delete_many({})
                
                message_to_output = "Wiped database."

                session.player_username = None
                session.characters = None
                session.the_dungeon = None
                session.items = None
                session.director = None
                session.monster_list = None
        
        # Universal commands
        
        # Tells the user which location they are at
        if ("locate" in command) or ("location" in command):
            message_to_output = f"At the {session.character.location[0]}"
            if session.character.location[1] == "Combat":
                message_to_output += "\nYou're in combat!"

        # Display character info
        elif ("character" in command) or ("char" in command):
            message_to_output = str(session.character)

        # Display character stats
        elif ("statistics" in command) or ("stats" in command):
            message_to_output = str(session.character.stats())

        # Output equipment and inventory
        elif ("inventory" in command) or ("inv" in command):
            message_to_output = str(session.character.full_inventory())

        # Commands usable everywhere except the dungeon
        if session.character.location[0] != "Dungeon":
        
            # Go to the inn
            if ("go" in command) and ("inn" in command):
                old_location = session.character.location[0]
                session.character.location = ("Inn", "Exploration")
                message_to_output = f"Traveled from the {old_location} to the {session.character.location[0]}"

            # Go to the market
            elif ("go" in command) and ("market" in command):
                old_location = session.character.location[0]
                session.character.location = ("Market", "Exploration")
                message_to_output = f"Traveled from the {old_location} to the {session.character.location[0]}"
        
            # Go to the dungeon
            elif (("go" in command) or ("enter" in command))and ("dungeon" in command):
                session.character.location = ("Dungeon", "Exploration")
                message_to_output = f"You have entered the dungeon. {session.the_dungeon.get_room(0).description}"

        # Commands availabe in the Inn    
        if session.character.location == ["Inn", "Exploration"]:
            # Change character name
            if "change name to" in command:
                old_name = session.character.character_name
                new_name = command.split("change name to")[1].strip()
                new_name = string.capwords(new_name, sep = None)
                session.character.character_name = new_name
                message_to_output = f"Name changed from '{old_name}' to '{new_name}'."

            # Change character description    
            elif ("change description to" in command):
                old_description = session.character.character_description
                new_description = command.split("change description to")[1].strip()
                new_description = string.capwords(new_description, sep = None)
                session.character.character_description = new_description
                message_to_output = f"Description changed from '{old_description}' to '{new_description}'."

            # Level up the character, spending experience equal to level
            elif ("level up" in command):
                level_selection = command.split("level up")[1].strip()
                if session.character.experience >= session.character.level:
                    session.character.experience -= session.character.level
                    new_level = session.character.level + 1
                    old_level = session.character.level
                    message_to_output = f"Description changed from '{old_level - 1}' to '{new_level}'."
                    if level_selection == "health":
                        session.character.current_health += 1
                        session.character.max_health += 1
                    elif level_selection == "intelligence":
                        session.character.intelligence += 1
                    elif level_selection == "strength":
                        session.character.strength += 1
                    elif level_selection == "dexterity":
                        session.character.dexterity += 1

            elif ("rest" in command) or ("sleep" in command) or ("heal" in command):
                if session.character.gold >= 5:
                    session.character.gold -= 5
                    session.character.current_heath = session.character.max_heath
                    message_to_output = (f"You spent 5 gold and has recovered to {session.character.current_heath} health!")
                else:
                    message_to_output = (f"You don't have enough gold to stay the night.")

        # Dungeon-only commands
        elif session.character.location[0] == "Dungeon":
            if ("room" in command):
                message_to_output = str(session.the_dungeon.get_room(session.character.dungeon_room))

            # Out-of-combat only commands

            # Escape the dungeon
            if (session.character.location[1] == "Exploration"):
                if ("leave" in command) or ("exit" in command) or ("escape" in command):
                    message_to_output = f"You've left the dungeon. You reached room {session.character.dungeon_room}. Returning to inn."
                    session.character.dungeon_room = 0
                    session.character.location = ("Inn", "Exploration")
                
                # The command to enter the first door
                elif (("door" in command) and ("1" in command)) or ("d1" in command):
                    # description_id_and_combat returns a tupple with the relevant data from changing rooms
                    # [0] is the string description of events
                    # [1] is the room_id to assign to the player depending on if they correctly chose an exit
                    # [2] is a boolean measuring if they entered combat or not, changing character.location[1] if so
                    description_id_and_combat = utilities.move_room(session.the_dungeon, session.character.dungeon_room, 1, session.director, session.items, session.monster_list, session)
                    session.character.dungeon_room = description_id_and_combat[1]
                    if description_id_and_combat[2]:
                        session.character.location = ("Dungeon", "Combat")
                    message_to_output = description_id_and_combat[0]

                # The command to enter the second door
                elif (("door" in command) and ("2" in command)) or ("d2" in command):
                    description_id_and_combat = utilities.move_room(session.the_dungeon, session.character.dungeon_room, 2, session.director, session.items, session.monster_list, session)
                    session.character.dungeon_room = description_id_and_combat[1]
                    if description_id_and_combat[2]:
                        session.character.location = ("Dungeon", "Combat")
                    message_to_output = description_id_and_combat[0]

                # The command to enter the third door
                elif (("door" in command) and ("3" in command)) or ("d3" in command):
                    description_id_and_combat = utilities.move_room(session.the_dungeon, session.character.dungeon_room, 3, session.director, session.items, session.monster_list, session)
                    session.character.dungeon_room = description_id_and_combat[1]
                    if description_id_and_combat[2]:
                        session.character.location = ("Dungeon", "Combat")
                    message_to_output = description_id_and_combat[0]

                elif ("search" in command) or ("loot" in command) or (command == "s"):
                    if session.the_dungeon.get_room(session.character.dungeon_room).searched == False:
                        session.the_dungeon.get_room(session.character.dungeon_room).searched = True
                        if utilities.target_check(session.character.intelligence):
                            session.character.gold += random.randint(1,6)
                            message_to_output = f"You now have {session.character.gold} gold!"
                        else:
                            message_to_output = f"You found nothing..."
                    else:
                        message_to_output = f"You found nothing..."

            elif session.character.location[1] == "Combat":
                if (command == "attack") or (command == "a"):
                    return_data = combat.fight("attack", session)
                    message_to_output = return_data[0]
                    if return_data[1] == "Monster":
                        message_to_output += "\nThe monster was defeated! You may proceed."
                        session.character.location[1] = "Exploration"
                    elif return_data[1] == "Character":
                        message_to_output += f"\n{session.character.character_name} was defeated!"
                        characters_collection.delete_one({"discord_username": session.player_username})
                        session.player_username = None
                    else:
                        message_to_output += "\nThe fight continues."

                elif (command == "fast") or (command == "f"):
                    return_data = combat.fight("fast", session)
                    message_to_output = return_data[0]
                    if return_data[1] == "Monster":
                        message_to_output += "\nThe monster was defeated! You may proceed."
                        session.character.location[1] = "Exploration"
                    elif return_data[1] == "Character":
                        message_to_output += f"\n{session.character.character_name} was defeated!"
                        characters_collection.delete_one({"discord_username": session.player_username})
                        session.player_username = None
                    else:
                        message_to_output += "\nThe fight continues."

                elif (command == "heavy") or (command == "h"):
                    return_data = combat.fight("heavy", session)
                    message_to_output = return_data[0]
                    if return_data[1] == "Monster":
                        message_to_output += "\nThe monster was defeated! You may proceed."
                        session.character.location[1] = "Exploration"
                    elif return_data[1] == "Character":
                        message_to_output += f"\n{session.character.character_name} was defeated!"
                        characters_collection.delete_one({"discord_username": session.player_username})
                        session.player_username = None
                    else:
                        message_to_output += "\nThe fight continues."

                elif ("run" in command) or ("escape" in command):
                    message_to_output += f"\n{session.character.character_name} attempts to escape. The monster makes your escape painful!"
                    combat.deal_damage(session.character, (random.randint(1, 6)), "attack")
                    if session.the_dungeon.get_room(session.character.dungeon_room).trap == True:
                        message_to_output += f"\nA trap triggers upon escape!"
                        if target_check(session.character.dexterity):
                            message_to_output += f"\n{session.character.character_name} evades the trap!"
                            message_to_output = f"You've left the dungeon. You reached room {session.character.dungeon_room}. Returning to inn."
                            session.character.dungeon_room = 0
                            session.character.location = ("Inn", "Exploration")
                        else:
                            message_to_output += f"\nThe trap is triggered!"
                            damage = random.randint(1, 6)
                            message_to_output += f"\n{session.character.character_name} takes {damage} damage!"
                            session.character.current_health -= damage       
                    if session.character.current_health <= 0:
                        message_to_output += f"\n{session.character.character_name} was defeated!"
                        characters_collection.delete_one({"discord_username": session.player_username})
                        session.player_username = None
                    else:
                        message_to_output = f"You've left the dungeon. You reached room {session.character.dungeon_room}. Returning to inn."
                        session.character.dungeon_room = 0
                        session.character.location = ("Inn", "Exploration")

    
        # Modifies the message_to_output variable of the session
        session.modify_output_text(message_to_output)
        return session
    
    except Exception:
        traceback.print_exc()
        session.modify_output_text("Sorry, that caused an error.")
        return session