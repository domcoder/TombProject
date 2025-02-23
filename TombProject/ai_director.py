# ai_director.py
print("\n Initialising ai_director.py")
# A decision maker that affects monsters, player luck and the dungeon

import utilities
import random
import dungeon
import monsters

class AiDirector:
    def __init__(self, unexplored_doors, total_monsters, total_rooms, difficulty, luck):
        self.director_name = "Director Vulture"
        self.unexplored_doors = int(unexplored_doors)
        self.total_monsters = int(total_monsters)
        self.total_rooms = int(total_rooms)
        self.difficulty = int(difficulty)
        self.luck = int(luck)

    def to_dict(self):
        return {
            "director_name": self.director_name,
            "unexplored_doors": self.unexplored_doors,
            "total_monsters": self.total_monsters,
            "total_rooms": self.total_rooms,
            "difficulty": self.difficulty,
            "luck": self.luck
        }

    def choose_monster(self, monster_room, items):
        if self.difficulty == 1:
            return monsters.random_monster(monster_room, items)
        elif self.difficulty == 2:
            pass

        elif self.difficulty == 3:
            pass

    def generate_room(self, new_room_id, item_list):
        # A decision-maker for how many exits a room has, based on the total number of available paths
        # The goal is to always have at least two paths and not more than 6
        room_count_options = [[], [1], [1, 2], [1, 2, 3]]
        if self.unexplored_doors <= 4:
            weights = [0, 1, 2, 2]
        elif self.unexplored_doors <= 6:
            weights = [1, 2, 2, 1]
        elif self.unexplored_doors <= 8:
            weights = [1, 1, 0, 0]
    
        # The number of doors in the room
        num_room_doors = random.choices(room_count_options, weights=weights, k=1)[0]

        # Generate room exits based on the number of doors
        room_exits = [self.total_rooms + exit_index for exit_index in num_room_doors]

        # Adds to the total rooms and unexplored rooms for calculations
        self.total_rooms = self.total_rooms + len(num_room_doors)
        self.unexplored_doors = self.unexplored_doors + (len(num_room_doors) -1)

        # A decision maker for monsters in rooms
        if self.total_monsters >= (self.total_rooms // 2):
            monster_target = 4
        else:
            monster_target = 7

        # Add monster to room
        if utilities.target_check(monster_target):
            print("A monster was spawned!")
            monster_in_room = self.choose_monster(new_room_id, item_list)
        else:
            print("No monsters were spawned.")
            monster_in_room = monsters.none_monster(new_room_id)

        if monster_in_room:
            self.total_monsters += 1
        trap_in_room = "None" if utilities.target_check(self.luck) else "Trap"
        treasure_in_room = "Treasure" if utilities.target_check(5) else "None"
        
        new_room = dungeon.Room(new_room_id, "Add description.", monster_in_room, trap_in_room, treasure_in_room, room_exits, False)
        print("New room V")
        print(new_room)

        # Must be done last once all data is decided and room is made
        new_room.description = utilities.generate_room_description(new_room)

        return new_room, monster_in_room