# monsters.py
print("\n Initializing monsters.py")
# A database of monsters

import combat
import item
import utilities
import random

class Monster:
    def __init__(self, name, health, skill, weapon, armour, room, description):
        self.name = name
        self.health = health
        self.skill = skill
        self.weapon = weapon
        self.armour = armour
        self.room = room
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "skill": self.skill,
            "weapon": self.weapon,
            "armour": self.armour,
            "room": self.room,
            "description": self.description 
        }

    def take_damage(self, damage):
        self.health -= damage

    def attack(self):
        # Implement monster's attack logic here
        pass

def none_monster(room):
    return Monster("None", 0, 0, item.Item("None", "None", "None", "None", 0, 0, "None", "None", "None", "None"), item.Item("None", "None", "None", "None", 0, 0, "None", "None", "None", "None"), room, "No monster.")

def random_monster(room, item_list):
    choice = random.randint(1, 3)
    if choice == 1:
        return skellington(room, item_list)
    elif choice == 2:
        return ghostlington(room, item_list)
    elif choice == 3:
        return corpseington(room, item_list)

# Balanced attack focus - tend towards balanced attacks, weak to crushing damage, resistent to piercing
# Sketelon
def skellington(monster_room, item_list):
    # Will need to make the spear an object
    joke = ""
    if utilities.target_check(2):
        joke = random.choice([" It looks like it has a bone to pick with you.", " Grinning menacingly, you know it's bad to the bone.", 
                              " 'Bone voyage.' It mutters under its breath.", " It skull-ks around in the shadows.", 
                              " 'This is going to be a skele-ton of fun.' It murmers to itself."])
    weapon_item = utilities.find_item_by_name(item_list, "Spear")
    armour_item = utilities.find_item_by_name(item_list, "Wool Gambeson")

    return Monster("Skeleton", 10, 6, weapon_item, armour_item, monster_room, f"A skeleton wielding a {weapon_item.item_name} in a {armour_item.item_name}.{joke}")
# Skeleton Warrior

# Skeleton Champion

# Fast attack focus - tend towards fast attacks, not much health & low armour
# Ghost
def ghostlington(monster_room, item_list):
    weapon_item = utilities.find_item_by_name(item_list, "Spectral Claws")
    armour_item = utilities.find_item_by_name(item_list, "None")
    return Monster("Skeleton", 6, 8, weapon_item, armour_item, monster_room, f"A transparent ghost.")

# Shade

# Phantom

# Heavy attack focus - tend towards heavy attacks, lots of health
# Shambling Corpse
def corpseington(monster_room, item_list):
    weapon_item = utilities.find_item_by_name(item_list, "Ghoulish Claws")
    armour_item = utilities.find_item_by_name(item_list, "None")
    return Monster("Skeleton", 12, 5, weapon_item, armour_item, monster_room, f"A semi-sentient corpse, dragging its feet.")

# Walking Corpse

# Animated Corpse

# Magic Focus - Unsure
# Utility Focus - Has a strange offhand item that changes the battle
# Curse Focus - cast a ritual to permenantly change the character