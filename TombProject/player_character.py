# player_character.py
print("\n Initialising player_character.py")
# The player character class

import item

class PlayerCharacter:
    def __init__(self, discord_username, character_name, character_description, current_health, max_health, strength, dexterity, intelligence, equipped_weapon, offhand_item, equipped_armour, equipped_talisman, experience, level, gold, inventory, location, dungeon_room):
        
        # Identification notes
        self.discord_username = discord_username

        # Name and description
        self.character_name = character_name
        self.character_description = character_description

        # Core stats
        self.current_health = current_health
        self.max_health = max_health
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

        # Equipped items
        # All are currently weapons, must be changed to their true types #
        self.equipped_weapon = equipped_weapon
        self.offhand_item = offhand_item
        self.equipped_armour = equipped_armour
        self.equipped_talisman = equipped_talisman
        
        # Resources
        self.experience = experience
        self.level = level
        self.gold = gold

        # Misc
        self.inventory = inventory
        self.location = location
        self.dungeon_room = dungeon_room

    # Set's the character's dungeon room to the input
    def set_room(self, room):
        self.dungeon_room = room

    # Add an item to their inventory
    # List the names of all items in their inventory

    # Prints the core character information
    def __str__(self):
        return (f"{self.character_name}, {self.character_description} \nHealth: {self.current_health} / {self.max_health} \nEquipment: {self.equipped_weapon.to_name()}, {self.offhand_item.to_name()}, {self.equipped_armour.to_name()}, {self.equipped_talisman.to_name()}")

    def stats(self):
        return (f"{self.character_name} \nHealth: {self.current_health} / {self.max_health} \nStrength: {self.strength}\nDexterity: {self.dexterity}\nIntelligence: {self.intelligence}\nGold: {self.gold}, Level {self.level}, Experience: {self.experience}")
        
    # Converts a character to a dictionary for MongoDB uploading
    def to_dict(self):
        return {
            "discord_username": self.discord_username,
            "character_name": self.character_name,
            "character_description": self.character_description,
            "current_health": self.current_health,
            "max_health": self.max_health,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "intelligence": self.intelligence,
            "equipped_weapon": self.equipped_weapon,
            "offhand_item": self.offhand_item,
            "equipped_armour": self.equipped_armour,
            "equipped_talisman": self.equipped_talisman,
            "experience": self.experience,
            "level": self.level,
            "gold": self.gold,
            "inventory": self.inventory,
            "dungeon_room": self.dungeon_room,
            "location": self.location
        }

    def full_inventory(self):
        return (f"Equipment: {self.equipped_weapon.to_name()}, {self.offhand_item.to_name()}, {self.equipped_armour.to_name()}, {self.equipped_talisman.to_name()}\nInventory: TODO")
 