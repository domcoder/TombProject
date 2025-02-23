# dungeon.py
print("\n Initializing dungeon.py")
# The dungeon and room class

class Room:
    def __init__(self, room_id, description, monster, trap, treasure, exits, searched):
        self.room_id = room_id
        self.description = description
        self.monster = monster
        self.trap = trap
        self.treasure = treasure
        self.exits = exits if exits is not None else []
        self.searched = searched

    def __str__(self):
        print(f"Debug: self.monster is of type {type(self.monster)} and value {self.monster}")
        if len(self.exits) == 1:
            exit_exits = "exit"
        else:
            exit_exits = "exits"
        if self.monster.name == "None":
            monster_check = "nothing in the room."
        else:
            if self.monster.health == 0:
                monster_check = f"a dead {self.monster.name} in the room."
            else:
                monster_check = f"a {self.monster.name} in the room!"

        return (f"{self.description}\nThere's {monster_check}\nThe room has {len(self.exits)} {exit_exits}.")

    def add_exit(self, exit_room_id):
        self.exits.append(exit_room_id)

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "description": self.description,
            "monster": self.monster,
            "trap": self.trap,
            "treasure": self.treasure,
            "exits": self.exits,
            "searched": self.searched
        }

class Dungeon:
    def __init__(self):
        self.rooms = []

    def add_room(self, new_room):
        self.rooms.append(new_room)

    def get_room(self, search_id):
        for room_obj in self.rooms:
            if room_obj.room_id == search_id:
                return room_obj
        return None

    def return_rooms(self):
        return self.rooms