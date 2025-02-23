# text_list.py
print("\n Initialising text_list.py")
# Several lists of text for two core functions:
    # Ensuring user inputs can use natural, varied language for inputs though this feature may be removed for complexity
    # Generating random names and descriptions

import random

def return_as_string(word_list):
    return " ".join(word_list)

def pick_random(word_list):
    return random.choice(word_list)


character_synonym = ["character", "char", ]

# A list of rooms for the player to explore
generic_room = ["A dimly lit chamber with a solitary stained glass window casting colourful patterns on the floor.",
                "A cavernous room with phosphorescent fungi illuminating the walls with an eerie glow.",
                "A circular chamber with a crumbled spiral staircase.",
                "A chamber with a shallow pool of water in the centre, its surface reflecting distorted images.",
                "A room with intricately carved pillars, remnants of a forgotten civilization.",
                "An abandoned laboratory filled with alchemical apparatuses and bubbling cauldrons.",
                "A dusty crypt with ancient sarcophagi lining the walls, each bearing mysterious inscriptions.",
                "A chamber with towering shelves filled with dusty tomes and scrolls, their contents waiting to be deciphered.",
                "A chamber with a large, ornate fountain at its centre, its waters long dried up.",
                "A chamber with a collapsed ceiling, moonlight streaming in through the cracks above."
                "A dark, grimy room with cobwebs in the corners and a musty smell lingering in the air.",
                "An open chamber with gently smoking torch sconces.",
                "A poorly lit room with damp walls and the sound of dripping water echoing in the distance.",
                "A rectangular, stone room adorned with ancient runes etched into the walls, their meaning long forgotten."]

zero_door_room = ["A long room with a dilapidated throne at one end, surrounded by tattered banners.",
                  "A grand hall with a crumbling chandelier hanging precariously from the ceiling.",
                  "A ballroom with faded tapestries depicting scenes of opulence and grandeur.",
                  "A banquet hall with long-abandoned tables covered in dust and cobwebs.",
                  "A library with shelves filled with ancient scrolls and forbidden knowledge.",
                  "A gallery with faded portraits of noble ancestors lining the walls.",
                  "A study with a desk covered in yellowed parchment and ink-stained quills.",
                  "A chapel with broken pews and stained glass windows depicting saints of old.",
                  "A torture chamber with rusty implements hanging from the walls, remnants of a cruel past.",
                  "A mausoleum with rows of stone coffins, their occupants long forgotten."
                  "A dilapidated kitchen with rusted pots and pans strewn about and a foul stench of decay.",
                  "A bedroom filled with dusty sleeping mats, the remnants of long-gone occupants.",
                  "A room filled with rows and rows of books, their pages yellowed with age and their spines cracked.",
                  "Walls closely surrounding a table with a single glass orb on it, emitting a faint, ethereal glow.",
                  "A room containing two armour-wearing dummies, their metal surfaces dented and scratched from countless training sessions.",
                  "A hallway, barricaded with chunks of stone and wood, evidence of a past struggle or siege.",
                  "A room filled with now-disused weapon racks, the weapons rusted and forgotten.",
                  "Rows upon rows of prison cells, the cold iron bars bearing witness to untold stories of captivity and despair."]

zero_door_confirmation = ["It's a dead end.", "No doors lead away from here.", "This dungeon path ends here.", "You can't go anywhere else from here.",
                          "No doors. Time to head back."]

one_door_room = ["A treasure vault with piles of gold coins and glittering jewels scattered across the floor.",
                 "A hidden chamber with a mysterious altar surrounded by flickering candles.",
                 "A secret passage with hidden compartments containing long-lost artifacts.",
                 "A wizard's laboratory with bubbling cauldrons and crackling electrical apparatuses.",
                 "A chamber with a magical portal shimmering with otherworldly energy.",
                 "A chamber with a hidden trapdoor leading to a labyrinthine maze below.",
                 "A hidden shrine with offerings left by devoted worshippers.",
                 "A chamber with ancient murals depicting scenes of forgotten lore.",
                 "A hidden library with forbidden tomes bound in human skin.",
                 "A chamber with a hidden alcove containing a sleeping dragon."
                 "A long corridor stretching into the darkness, its walls adorned with faded tapestries depicting heroic deeds of old.",
                 "A narrow passage lined with flickering torches.",
                 "A small chamber with a single exit.",
                 "A dimly lit room with a solitary doorway.",
                 "A cramped space leading to a solitary exit."]

one_door_confirmation = ["This room is a corridor, only one way to go.", "Only one door ahead." "Two doors but the second is stuck fast. Only one way to go.",
                         "You notice a door hidden behind an out-of-place bookshelf.", 
                         "You turn around to see that the door you just came from stretches into a room you've definitely never been in before."
                         "There's only one way to go."]

two_door_room = ["A chamber with two ornately carved doors, each leading to unknown destinations.",
                 "A junction with two paths diverging.",
                 "A crossroads with two doors to choose from.",
                 "A chamber with dual exits.",
                 "An intersection with two possible routes."]

two_door_confirmation = ["The room junctions towards two sepeate paths.", "Two doors ahead. Pick wisely." "Two doors but one is very rusty. You can force it open, though.",
                         "You find two doors behind large curtains.", "You blink and two doors appear. You're certain they weren't there before."
                         "There are two ways to go."]

three_door_room = ["A large chamber with three towering doorways, each shrouded in mystery and beckoning exploration.",
                   "A hub with three doorways branching out.",
                   "A central room with three potential exits.",
                   "A nexus with three paths leading away.",
                   "A junction point offering three choices of passage."]

three_door_confirmation = ["The room junctions towards three sepeate paths.", "Thee doors ahead. Lots of choice." "Three doors. One is made of bronze, another iron and the last is made of... mud?",
                         "Someone tried to hide all three doors behind a stack of crates that towers to the ceiling.", "Three doors. They all give off 'bad vibes'."
                         "There are three ways to go."]

notable_room_objects = ["A broken sword", "A dusty tome bound in cracked leather", "A shattered potion vial", "A wood-wrought crown", 
                        "A wooden chalice", "A mysterious key with ornate carvings", "A once-glowing crystal orb",
                        "A tattered map depicting lands", "A cracked hourglass with its sands frozen in time", "A rusted chest, laying ransacked and looted",
                        "A dusty tapestry depicting a heroic battle between humans and monsters", "A polished glass bead reflecting a mesmerizing kaleidoscope of colours",
                        "A rusted lantern with no oil", "A weathered cloak", "A tarnished locket with an engraved portrait inside",
                        "A set of ancient runes carved into stone tablets", "A faded journal filled with cryptic entries", "A worn-out pair of leather boots",
                        "A blunt, blood-stained dagger", "A set of skeleton keys", "A glimmering gemstone", "A tarnished silver goblet", 
                        "A cracked porcelain doll with missing limbs", "A bundle of dried herbs tied with fraying string", "A tarnished mirror reflecting distorted images",
                        "A worn-out banner bearing the emblem of a forgotten kingdom", "A rusted suit of armor missing its helm",
                        "A small, intricately carved figurine of a dragon", "A faded tapestry depicting a majestic landscape"]

object_locations = ["sitting on a stool.", "embedded in a stone pedestal.", "resting atop a weathered skeleton's skull.", "dangling from a nail in a table.",
                    "tucked into a shelf.", "propped against a crumbling wall.", "half-buried in the dirt floor.", "hidden in a nook in the wall.",
                    "nestled in a pile of old rags.", "perched on a rotting wooden beam.", "entangled in the roots caving in the north wall.",
                    "wedged between two large, shapeless rocks.", "submerged in a shallow pool of water.", "entombed within a sarcophagus.", 
                    "concealed beneath a tattered tapestry.", "balanced precariously on a ledge.", "resting on a makeshift altar.",
                    "suspended from the ceiling by a threadbare rope.", "buried beneath a layer of dust.",
                    "resting on a moss-covered pedestal.", "protruding from a pile of rubble.", "enshrined within a crumbling birds nest.",
                    "nestled within the coils of a serpent statue.", "perched atop a crumbling pillar.",
                    "concealed behind a false door.", "half-submerged in a murky puddle.", "hanging from the rafters.",
                    "wedged between the pages of a dusty tome lying open on the floor.", "balancing on a chair.", "hanging from a hook.", "embedded in a rough stone wall"]

object_actions = ["It rolls around as if just recently disturbed.", "An acrid mist slightly drifts from it.", "Residue of a swirling, iridescent liquid drips from it.",
                  "It is adorned with intricate engravings of mythical creatures.", "You've never seen anything like this before.",
                  "It shifts in a breeze you don't feel.", "It hums with latent magical energy... oh wait it's just a cicada.",
                  "An arrow sticks out of it.", "Pages with mad scribblings almost bury it.", "You barely make out a small bell on a string attached to it.",
                  "It's wet. Very wet.", "A miniature replica carved out of ivory sits propped up beside it."]