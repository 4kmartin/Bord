from Characters.character import *
from Items.items import *
from World.world import *
from random import choice
from command_parser import *

disclaimer = """ 
    BORD! Copyright (C) 2021 Anthany Martin
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it.
    """

def main(level=Level(),npcs=[]):
    print(disclaimer)
    player = setupPlayer()
    gameLoop(player, level, npcs)
    

def roll(faces = 20):
    return choice(range(1,faces+1))

def attack(player: Character, tokens, npcs:dict,weapon = 0):
    if tokens[1] in npcs.keys():
        if npcs[tokens[1]].location == player.location:
            hit = player.hit(roll(),weapon)
            npcs[tokens[1]].health -= hit
            print("you attack a %s for %s points of damage.\nThe %s has %s/100 health" % (tokens[1], hit,tokens[1],npcs[tokens[1]].health))
            if npcs[tokens[1]].health < 1:
                print("You have defeated the %s" % tokens[1])
                npcs.pop(tokens[1])
        else:
            raise IOError
    else:
        raise IOError
    

def setupPlayer()->Character:
    print("what is you name?:")
    player_name = input()
    return assignClass(player_name)    

def assignClass(player_name)->Character:
    print("Please select your class. \nChoose either; Warior, Explorer or Scholar:")
    player_class = input()
    if player_class in ("w","W","warior","Warior","WARIOR"):
        return Warior(player_name)
    elif player_class in ("e","E","explorer","Explorer","EXPLORER"):
        return Explorer(player_name)
    elif player_class in ("s","S","scholar","Scholar","SCHOLAR"):
        return Scholar(player_name)
    else:
        print("Something went wrong lets try again")
        assignClass(player_name)

def update(level:Level, npcs:dict, player):
    for tile in level:
        tile.update()
    for npc in npcs.values():
        npc.turn(player, roll())

def gameLoop(player:Character, level:Level, npcs):
    while True:
        loc = level.level_map[player.location[0]][player.location[1]]
        print(loc.biome.description)
        if len(loc.visible) > 0:
            print("You see:")
            for item in loc.visible:
                print(item.description)
        player_turn(player,level, npcs)
        update(level, npcs, player)
        if player.health < 1:
            print("%s, you have died. GAME OVER" % player.name)
            print("%s- strength: %s speed: %s smarts: %s" % (player.name, player.strength,player.speed,player.smarts))
            break
        if len(npcs) < 1:
            print("You are victorious")
            break

def get_command(player:Character,level:Level, npcs):
    tokens = normalize(tokenize(input("%s :>" % player.name)),default_thesaurus)
    if len(tokens)<2:
        if tokens[0] == "quit":
            quit()
        else:
             raise IOError
    if tokens[0] == "go":
        move(player,tokens,level)
    elif tokens[0] == "get":
        get_status(player, tokens)
    elif tokens[0] == "attack":
        attack(player,tokens, npcs)
    elif tokens[0] == "use":
        use_item(player,tokens,npcs)
    else:
        raise IOError

def move(player:Character, tokens, level:Level):
    if len(tokens) > 2 or len(tokens) < 1:
        raise IOError
    else:
        old_location = player.location.copy()
        player.move(tokens[1])
        if outside_of_map(player, level):
            print("You can't go that way")
            player.location = old_location

def get_status(player:Character,tokens):
    if len(tokens) > 2:
        raise IOError
    elif len(tokens) == 2:
        _ = {
            "coords": player.location,
            "health": player.health,
            "inventory":str(list(player.items.values())),
        }
        if tokens[1] in _.keys():
           print(_[tokens[1]])
    else:
        raise IOError


def player_turn(player, level, npcs):
    try:
        get_command(player, level, npcs)
    except IOError:
        print("something went wrong, try again")
        get_command(player, level, npcs)

def use_item(player,tokens,npcs):
    try:
        if tokens[1] in player.items.keys():
            item = player.items[tokens[1]]
            if item.__class__ is Weapons:
                tokens.remove(tokens[1])
                attack(player, tokens, npcs, item.attack)
            else:
                raise IOError
        else:
            raise IOError
    except IndexError:
        raise IOError

def outside_of_map(player:Character, level: Level) -> bool:
    return player.location[0] > len(level.level_map)-1 or player.location[1] > len(level.level_map[0])-1


if __name__ == "__main__":

    forest = Biome()
    forest.description = "You are in a Forest"
    forest.passable = True
    
    l = [
        [Tile(biome=forest),Tile(biome=forest),Tile(biome=forest)],
        [Tile(biome=forest),Tile(biome=forest),Tile(biome=forest)],
        [Tile(biome=forest),Tile(biome=forest),Tile(biome=forest)]
        ]
    level = Level().manual(l)

    gru = NPC("gru", [2,2])
    npcs={
        gru.name:gru,
    }

    main(level, npcs)