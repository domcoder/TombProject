import utilities
import player_character
import random
import re

def calculate_damage(damage_str):
    # Use regular expression to parse the damage string
    match = re.match(r'(\d+)d([+-]?\d*)', damage_str)
    if not match:
        raise ValueError(f"Invalid damage string format: {damage_str}")
    
    num_dice = int(match.group(1))
    bonus_str = match.group(2)
    
    # If the bonus string is empty, default to 0
    bonus = int(bonus_str) if bonus_str else 0

    # Roll the dice
    dice_total = sum(random.randint(1, 6) for _ in range(num_dice))
    
    # Add the bonus or penalty
    total_damage = dice_total + bonus
    
    return total_damage

def deal_damage(entity, damage, attack_type):
    if isinstance(entity, player_character.PlayerCharacter):
        base_damage = max(0, damage - entity.equipped_armour.damage_reduction)
        new_damage = base_damage + (entity.strength - 5)
        print(f"Damage roll = max(0, ({damage} - {entity.equipped_armour.damage_reduction})) + ({entity.strength - 5})")
        print(f"Dealing {new_damage} damage to {entity.character_description} who's current health is {entity.current_health} (armour = {entity.equipped_armour})")
        entity.current_health -= new_damage
        print(f"New health = {entity.current_health}")
    else:
        base_damage = max(0, damage - entity.armour.damage_reduction)
        new_damage = base_damage + (entity.skill - 5)
        print(f"Dealing {new_damage} damage to {entity.description} who's current health is {entity.health}")
        
        if attack_type == "heavy":
            new_damage = int(new_damage * 2.5)
        elif attack_type == "fast":
            new_damage = max(0, new_damage - (entity.strength - 5))
        
        entity.health -= new_damage
        print(f"New health = {entity.health}")
        
    return new_damage

def speed_contest(monster, character, attack_type):
    speed_modifier = {"fast": 2, "heavy": -2}.get(attack_type, 0)
    if (monster.skill // 3) > ((character.dexterity // 3) + speed_modifier):
        return "monster"
    else:
        return "character"

def to_hit_check(attacker, defender, attack_type):
    if isinstance(attacker, player_character.PlayerCharacter):
        if utilities.target_check(attacker.dexterity) and not utilities.target_check(defender.skill):
            damage_str = attacker.equipped_weapon.damage
            print(f"Player's damage string: {damage_str}")
            damage = calculate_damage(damage_str)
            return f"\n{deal_damage(defender, damage, attack_type)} damage was dealt to {defender.name}!"
        else:
            return f"\n{attacker.character_name} missed!"
    else:
        if utilities.target_check(attacker.skill) and not utilities.target_check(defender.dexterity):
            damage_str = attacker.weapon.damage
            print(f"Monster's damage string: {damage_str}")
            damage = calculate_damage(damage_str)
            return f"\n{deal_damage(defender, damage, attack_type)} damage was dealt to {defender.character_name}!\n{defender.character_name} now has {defender.current_health} / {defender.max_health} health."
        else:
            return f"\n{attacker.name} missed!"

def fight(attack_type, session):
    combat_log = ''
    room_monster = session.the_dungeon.get_room(session.character.dungeon_room).monster
    combat_end = "None"

    if speed_contest(room_monster, session.character, attack_type) == "monster":
        combat_log += f"The {room_monster.name} is faster!"
        combat_log += to_hit_check(room_monster, session.character, attack_type)
        if attack_type == "heavy":
            combat_log += f"\nThe {room_monster.name} strikes again!"
            combat_log += to_hit_check(room_monster, session.character, attack_type)
        combat_log += to_hit_check(session.character, room_monster, attack_type)
    else:
        combat_log += f"{session.character.character_name} is faster!"
        combat_log += to_hit_check(session.character, room_monster, attack_type)
        combat_log += to_hit_check(room_monster, session.character, attack_type)
        if attack_type == "heavy":
            combat_log += f"\nThe {room_monster.name} strikes again!"
            combat_log += to_hit_check(room_monster, session.character, attack_type)

    if room_monster.health <= 0:
        combat_end = "Monster"
    elif session.character.current_health <= 0:
        combat_end = "Character"

    return [combat_log, combat_end]