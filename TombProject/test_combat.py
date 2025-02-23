import player_character

def calculate_damage(damage_str):
    match = re.match(r'(\d+)d(\d+)([+-]\d+)?', damage_str)
    if match:
        num_dice = int(match.group(1))
        dice_type = int(match.group(2))
        bonus = int(match.group(3)) if match.group(3) else 0

        dice_total = sum(random.randint(1, dice_type) for _ in range(num_dice))
        return dice_total + bonus

def deal_damage(entity, damage, attack_type):
    if type(entity) == player_character.PlayerCharacter:
        new_damage = max(0, (damage - entity.equipped_armour.damage_reduction)) + (entity.strength - 5)
        if attack_type == "heavy":
            new_damage = int(new_damage * 2.5)
        elif attack_type == "fast":
            new_damage = max(0, new_damage - entity.strength)
        entity.current_health -= new_damage
    else:
        new_damage = max(0, (damage - entity.armour.damage_reduction)) + (entity.skill - 5)
        entity.health -= new_damage
    return new_damage

def speed_contest(monster, character, attack_type):
    if attack_type == "fast":
        speed = 2
    elif attack_type == "heavy":
        speed = -2
    else:
        speed = 0

    if (monster.skill // 3) > ((character.dexterity // 3) + speed):
        return "monster"
    else:
        return "character"

def to_hit_check(attacker, defender, attack_type):
    if type(attacker) == player_character.PlayerCharacter:
        if (utilities.target_check(attacker.dexterity) == True) and (utilities.target_check(defender.skill) == False):
            return f"\n{deal_damage(defender, attacker.equipped_weapon, attack_type)} damage was dealt to {defender}!"
        else:
            return f"\n{attacker} missed!"
    else:
        if (utilities.target_check(attacker.skill) == True) and (utilities.target_check(defender.dexterity) == False):
            return f"\n{deal_damage(defender, attacker.weapon, attack_type)} damage was dealt to {defender}!"
        else:
            return f"\n{attacker} missed!"


if speed_contest(room_monster.name, session.character.dexterity, attack_type) == ("monster"):
    combat_log += f"The {room_monster.name} is faster!\n"
    combat_log += to_hit_check(room_monster, session.character, attack_type)
    if attack_type == "heavy":
        combat_log += f"The {room_monster.name} strikes again!\n"
        combat_log += to_hit_check(room_monster, session.character, attack_type)
    combat_log += to_hit_check(session.character, room_monster, attack_type)
else:
    combat_log += f"{session.character.character_name} is faster!\n"
    combat_log += to_hit_check(session.character, room_monster, attack_type)
    combat_log += to_hit_check(room_monster, session.character, attack_type)
    if attack_type == "heavy":
        combat_log += f"The {room_monster.name} strikes again!\n"
        combat_log += to_hit_check(room_monster, session.character, attack_type)




        if (utilities.target_check(room_monster.skill) == True) and (utilities.target_check(session.character.dexterity) == False):
            damage = utilities.deal_damage(session.character, utilities.calculate_damage(room_monster.weapon.damage)) + session.character.strength
            combat_log += f"The {room_monster.name} hits for {damage}!\n"
        else:
            combat_log += f"The {room_monster.name} misses!\n"
        if (utilities.target_check(session.character.dexterity) == True) and (utilities.target_check(room_monster.skill == False)):
            damage = utilities.deal_damage(room_monster, utilities.calculate_damage(session.chaeracter.equipped_weapon.damage))
            combat_log += f"{session.character.character_name} hits for {damage}!\n"
        else:
            combat_log += f"{session.character.character_name} misses!\n"
    else:
        if (utilities.target_check(session.character.dexterity) == True) and (utilities.target_check(room_monster.skill == False)):
            damage = utilities.deal_damage(room_monster, utilities.calculate_damage(session.chaeracter.equipped_weapon.damage))
            combat_log += f"{session.character.character_name} hits for {damage}!\n"
        else:
            combat_log += f"{session.character.character_name} misses!\n"
        if (utilities.target_check(room_monster.skill) == True) and (utilities.target_check(session.character.dexterity) == False):
            damage = utilities.deal_damage(session.character, utilities.calculate_damage(room_monster.weapon.damage))
            combat_log += f"The {room_monster.name} hits for {damage}!\n"
        else:
            combat_log += f"The {room_monster.name} misses!\n"