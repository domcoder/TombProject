# utilities.py
print("\n Initializing utilities.py")
# A number of utility functions to reduce clutter and increase robustness

import item
import player_character
import dungeon
import ai_director
import random
import text_list
import monsters
import re

# dictionary-to-item
def dict_to_item(item_dict):
    return item.Item(
        item_name=item_dict.get("item_name"),
        item_type=item_dict.get("item_type"),
        item_description=item_dict.get("item_description"),
        damage_type=item_dict.get("damage_type"),
        damage=item_dict.get("damage"),
        damage_reduction=item_dict.get("damage_reduction"),
        damage_resistance=item_dict.get("damage_resistance"),
        damage_vulnerability=item_dict.get("damage_vulnerability"),
        tags=item_dict.get("tags"),
        special=item_dict.get("special")
    )

# dictionary-to-character
def dict_to_player_character(character_dict):
    return player_character.PlayerCharacter(
        discord_username = character_dict.get("discord_username"),
        character_name = character_dict.get("character_name"),
        character_description = character_dict.get("character_description"),
        current_health = character_dict.get("current_health"),
        max_health = character_dict.get("max_health"),
        strength = character_dict.get("strength"),
        dexterity = character_dict.get("dexterity"),
        intelligence = character_dict.get("intelligence"),
        equipped_weapon = dict_to_item(character_dict.get("equipped_weapon")),
        offhand_item = dict_to_item(character_dict.get("offhand_item")),
        equipped_armour = dict_to_item(character_dict.get("equipped_armour")),
        equipped_talisman = dict_to_item(character_dict.get("equipped_talisman")),
        experience = character_dict.get("experience"),
        level = character_dict.get("level"),
        gold = character_dict.get("gold"),
        inventory = [dict_to_item(item_dict) for item_dict in character_dict.get("inventory", [])],
        location = character_dict.get("location")
    )
# dictionary-to-room
def dict_to_room(room_dict):
    return dungeon.Room(
        room_id = room_dict.get("room_id"),
        description = room_dict.get("description"),
        monster = room_dict.get("monster"),
        trap = room_dict.get("trap"),
        treasure = room_dict.get("treasure"),
        exits = room_dict.get("exits", []),
        searched = room_dict.get("searched")
    )

# dictionary-to-monster
def dict_to_monster(monster_dict):
    return monsters.Monster(
        name = monster_dict.get("name"),
        health = monster_dict.get("health"),
        skill = monster_dict.get("skill"),
        damage_type = monster_dict.get("damage_type"),
        armour = monster_dict.get("armour"),
        room = monster_dict.get("room"),
        description = monster_dict.get("description", [])
    )

# default character
def default_character(username): 
    return {
            "discord_username": username,
            "character_name": "Unnamed Adventurer",
            "character_description": "A dungeon-delving adventurer.",
            "current_health": 15,
            "max_health": 15,
            "strength": 7,
            "dexterity": 7,
            "intelligence": 7,
            "equipped_weapon": "Spear",
            "offhand_item": "Nothing",
            "equipped_armour": "New Tunic",
            "equipped_talisman": "Old Ring",
            "experience": 0,
            "level": 0,
            "gold": 0,
            "inventory": [],
            "location": ("Inn", "Exploration"),
            "dungeon_room": 0
        }

def return_none_monster(room):
    return monsters.none_monster(room)

# default room
def default_room():
    return {
            "room_id": 0,
            "description": "The great doors etched with arcane runes thunder closed behind you. The tunnel up ahead leads to a sturdy wooden door.",
            "monster": monsters.none_monster(0),
            "trap": "None",
            "treasure": "None",
            "exits": [1],
            "searched": True
        }

# default items
def default_items():
    return [
            {
                "item_name": "Spear",
                "item_type": "Weapon",
                "item_description": "A simple iron spear. Newly polished!",
                "damage_type": "piercing",
                "damage": "1d",
                "damage_reduction": 0,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "New Tunic",
                "item_type": "Armour",
                "item_description": "A brand new tunic! Unfortunately, it doesn't protect you.",
                "damage_type": "",
                "damage": "",
                "damage_reduction": 0,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "Old Ring",
                "item_type": "Misc",
                "item_description": "A treasured trinket from home.",
                "damage_type": "",
                "damage": "",
                "damage_reduction": 0,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "Nothing",
                "item_type": "",
                "item_description": "",
                "damage_type": "",
                "damage": "",
                "damage_reduction": 0,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "Chain Mail",
                "item_type": "Armour",
                "item_description": "Iron rings sewn to leather.",
                "damage_type": "",
                "damage": "",
                "damage_reduction": 4,
                "damage_resistance": "slashing",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "Wool Gambeson",
                "item_type": "Armour",
                "item_description": "A quilted jacket providing some protection.",
                "damage_type": "",
                "damage": "",
                "damage_reduction": 1,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "None",
                "item_type": "None",
                "item_description": "None",
                "damage_type": "",
                "damage": "",
                "damage_reduction": 0,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "Spectral Claws",
                "item_type": "Weapon",
                "item_description": "Ghostly talons made physical.",
                "damage_type": "Slashing",
                "damage": "1d-2",
                "damage_reduction": 0,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            },
            {
                "item_name": "Ghoulish Claws",
                "item_type": "Weapon",
                "item_description": "Rotting, sharp nails.",
                "damage_type": "Slashing",
                "damage": "1d",
                "damage_reduction": 0,
                "damage_resistance": "",
                "damage_vulnerability": "",
                "tags": "",
                "special": ""
            }
        ]

def default_director():
    return {
        "unexplored_doors": 1, 
        "total_monsters": 0, 
        "total_rooms": 1, 
        "difficulty": 1, 
        "luck": 10
        }

# Turns all equipment from strings to item objects
# Only called in download_database, instead create an item object (add it to session items) and equip if mid-game
def convert_equipment_name_to_item(character, current_item_list):
    for item_obj in current_item_list:
        if item_obj.item_name == character.equipped_weapon:
            character.equipped_weapon = item_obj
        if item_obj.item_name == character.offhand_item:
            character.offhand_item = item_obj
        if item_obj.item_name == character.equipped_armour:
            character.equipped_armour = item_obj
        if item_obj.item_name == character.equipped_talisman:
            character.equipped_talisman = item_obj

    # Failsafe if item name has not been found
    error_item = item.Item("Error", "None", "An error has corrupted this item.", "None", "0", 0, "-", "-", "-", "-")

    if character.equipped_weapon == str:
        print("Error weapon equipped.")
        character.equipped_weapon = error_item
    if character.offhand_item == str:
        print("Error offhand equipped.")
        character.offhand_item = error_item
    if character.equipped_armour == str:
        print("Error armour equipped.")
        character.equipped_armour = error_item
    if character.equipped_talisman == str:
        print("Error talisman equipped.")
        character.equipped_talisman = error_item

    return character

def convert_monster_items_to_item(monster, current_item_list):
    for item_obj in current_item_list:
        if item_obj.item_name == monster.weapon:
            monster.weapon = item_obj
    for item_obj in current_item_list:
        if item_obj.item_name == monster.armour:
            monster.armour = item_obj

def populate_dungeon_rooms_with_monsters(dungeon_rooms, monster_list):
    for each_room in dungeon_rooms:
        for each_monster in monster_list:
            if each_room.room_id == each_monster.room:
                each_room.monster = each_monster

# A description function that will eventually call on text_list.py to generate on-the-fly random room descriptions
def generate_room_description(room):
    description = ""
    num_doors = len(room.exits)
    if target_check(5) and (room.room_id != 0):
        if num_doors == 0:
            description = (f"{random.choice(text_list.zero_door_room)} {random.choice(text_list.notable_room_objects)} {random.choice(text_list.object_locations)} {random.choice(text_list.object_actions)} {random.choice(text_list.zero_door_confirmation)}")
        elif num_doors == 1:
            description = (f"{random.choice(text_list.one_door_room)} {random.choice(text_list.notable_room_objects)} {random.choice(text_list.object_locations)} {random.choice(text_list.object_actions)} {random.choice(text_list.one_door_confirmation)}")
        elif num_doors == 2:
            description = (f"{random.choice(text_list.two_door_room)} {random.choice(text_list.notable_room_objects)} {random.choice(text_list.object_locations)} {random.choice(text_list.object_actions)} {random.choice(text_list.two_door_confirmation)}")
        elif num_doors == 3:
            description = (f"{random.choice(text_list.three_door_room)} {random.choice(text_list.notable_room_objects)} {random.choice(text_list.object_locations)} {random.choice(text_list.object_actions)} {random.choice(text_list.three_door_confirmation)}")

    else:
        if num_doors == 0:
            description = "You enter a room with no doors. A dead end."
        elif num_doors == 1:
            description = "You enter a room with a single door."
        else:
            description = f"You enter a room with {num_doors} doors."

    # Check if there is a monster in the room
    if room.monster.name != "None":
        description += f" There is a menacing {room.monster.name} lurking inside! A fight has begun!"
    else:
        description += " The room appears to be empty."

    return description

# A function to procedurally generate a new room or simply move into it if it already exists
def move_room(current_dungeon, current_room_id, door_number_selected, director, item_list, monster_list, current_session):
    print(f"Moving room, monster_list debug: {monster_list}")
    # Stores the current room in current_room
    current_room = current_dungeon.get_room(current_room_id)
    combat_begins = False
    room_output = ["Error. Did not change room.", current_room_id, combat_begins]

    # If the current room exists in the dungeon list
    if current_room:

        # Exits = the list of the room's exit doors
        exits = current_room.exits
        
        # If the user has entered a valid door (1, 2 or 3 in rooms that have that many or less doors)
        if door_number_selected <= len(exits):

            # The next room's room_id equals whatever was stored in the door position they chose from the exits list (starts at 0)
            next_room_id = exits[door_number_selected - 1]

            # Searches for an existing room
            next_room = current_dungeon.get_room(next_room_id)
            if next_room:

                # If the room is found, it returns the next room's description alongside it's room_id so that the player's dungeon_room can be updated
                room_output = [next_room.description, next_room.room_id, False]
                # Monster fight logic
                if next_room.monster.name != "None":
                    print("There is a monster in this room. Combat beginning!")
                    # room_output[0] = room_output[0] + f"\nThere's a {next_room.monster.name} in the room!"
                    combat_begins = True
                print(f"Player is moving to room {next_room.room_id}")
                room_output = [next_room.description, next_room.room_id, combat_begins]
            else:
                
                # Generate a new room description and create a new room
                print("Room doesn't exist yet, generating a room.")
                new_room, new_monster = director.generate_room(next_room_id, item_list)
                current_session.monster_list.append(new_monster)

                # Add the new room to the dungeon
                current_dungeon.add_room(new_room)
                
                # Checks if there is a monster in it
                if new_room.monster.name != "None":
                    print("There is a monster in this room. Combat beginning!")
                    # room_output[0] = room_output[0] + f"\nThere's a {new_room.monster.name} in the room!"
                    combat_begins = True
                print(f"Player is moving to room {new_room.room_id}")
                room_output = [new_room.description, new_room.room_id, combat_begins]
        else:
            room_output = ["This room doesn't have that many doors.", current_room_id, combat_begins]
    else:
        room_output = ["Current room not found in the dungeon.", 0, combat_begins]
    return room_output

# Rolls two six-sided dice and comments on the result, sometimes
def fun_roll():
    num1, num2 = random.randint(1, 6), random.randint(1, 6)
    if num1 == 1 and num2 == 1:
        comment = " - Snake eyes!"
    elif num1 == num2:
        comment = " - Doubles!"
    elif num1 + num2 == 7:
        comment = " - Seven!"
    else:
        comment = ""
    return f"{num1}, {num2}" + comment

# The core dice roller
'''
Probabilities result or less:
2: 2.77%
3: 8.33%
4: 16.66%
5: 27.77%
6: 41.66%
7: 58.33%
8: 72.22%
9: 83.33%
10: 91.66%
11: 97.22%
12: 100%
'''
def roll():
    return (random.randint(1, 6) + random.randint(1, 6))

# A function that takes a target number as input
# It rolls 2d6 and if the result is lower than the target, it outputs True (a success)
# Otherwise, it outputs False meaning a failure
def target_check(target):
    return roll() <= target

def find_item_by_name(item_obj_list, search_id):
    for item_obj in item_obj_list:
        if item_obj.item_name == search_id:
            return item_obj
    return None
