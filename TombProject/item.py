# item.py
print("\n Initialising item.py")
# The class that covers all items

class Item:
    def __init__(self, item_name, item_type, item_description, damage_type, damage, damage_reduction, damage_resistance, damage_vulnerability, tags, special):
        
        # Name and description
        self.item_name = item_name
        self.item_type = item_type
        self.item_description = item_description

        # Core stats
        self.damage_type = damage_type
        self.damage = damage
        self.damage_reduction = damage_reduction
        self.damage_resistance = damage_resistance
        self.damage_vulnerability = damage_vulnerability

        # Misc info
        self.tags = tags
        self.special = special
        
    # Prints the core item information
    ## Currently tuned for wepaons only
    def __str__(self):
        return f"Name: {self.item_name}, Type: {self.item_type}, Description: {self.item_description}, \nDamage: {self.damage}, Damage Type: {self.damage_type}, Damage Reduction: {self.damage_reduction}, Damage Resistance: {self.damage_resistance}, Damage Vulnerability: {self.damage_vulnerability}, \nTags: {self.tags}, Special: {self.special}"

    def to_dict(self):
        return {
            "item_name": self.item_name,
            "item_type": self.item_type,
            "item_description": self.item_description,
            "damage_type": self.damage_type,
            "damage": self.damage,
            "damage_reduction": self.damage_reduction,
            "damage_resistance": self.damage_resistance,
            "damage_vulnerability": self.damage_vulnerability,
            "tags": self.tags,
            "special": self.special
        }

    def to_name(self):
        return self.item_name