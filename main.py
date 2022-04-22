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

commands = """
HELP                        GENERATES THIS MENU
QUIT                        TERMINATES THE GAME, NO PROGRESS IS SAVED
GO [DIRECTION]              MOVES THE PLAYER IN ANY CARDINAL DIRECTION
USE [ITEM, TARGET]          USES AN ITEM ON THE SPECIFIED TARGET
ATTACK [TARGET]             DO DAMAGE TO A SPECIFIED TARGET
"""



class Game:
    
    def __init__(self, player:Character, npcs: dict[NPC], level:Level):
        self.player = player
        self.npcs = npcs
        self.level = level
        self.tokens = [""]
        self.weapon = 0
        self.buffs = {
            'permanant':{},
            'temporary':{}
        }

    def roll(self, faces = 20):
        return choice(range(1,faces+1))

    def attack(self):
        if self.tokens[1] in self.npcs.keys():
            if self.npcs[self.tokens[1]].location == self.player.location:
                hit = self.player.hit(self.roll(),self.weapon)
                self.npcs[self.tokens[1]].takeDamage(hit) 
                print("you attack a %s for %s points of damage.\nThe %s has %s/100 health" % (self.tokens[1], hit,self.tokens[1],self.npcs[self.tokens[1]].health))
                if self.npcs[self.tokens[1]].getHealth() < 1:
                    print("You have defeated the %s" % self.tokens[1])
                    self.npcs.pop(self.tokens[1])
            else:
                raise IOError
        else:
            raise IOError

    def update(self):
        for tile in self.level:
            tile.update()
        for npc in self.npcs.values():
            npc.turn(self.player, self.roll())
        self.buffs["permanant"].clear()
        for buff in self.buffs["temporary"]:
            self.player.__dict__[buff] -= self.buffs["temporary"][buff]
        self.buffs["temporary"].clear()

    
    def gameLoop(self):
        while True:
            loc = self.level.getPosition(*self.player.getLocation())
            print(loc.getDescription())
            if len(loc.visible) > 0:
                print("You see:")
                for item in loc.visible:
                    print(item.description)
            self.player_turn()
            self.update()
            if self.player.health < 1:
                print("%s, you have died. GAME OVER" % self.player.name)
                print("%s- strength: %s speed: %s smarts: %s" % (self.player.name, self.player.strength,self.player.speed,self.player.smarts))
                break
            if len(npcs) < 1:
                print("You are victorious")
                break
    
    def get_command(self):
        tokens = normalize(tokenize(input("%s :>" % self.player.name)),default_thesaurus)
        self.tokens = tokens
        if len(tokens)<2:
            if tokens[0] == "quit":
                quit()
            elif tokens[0] == "help":
                print(commands)
            else:
                raise IOError
        if tokens[0] == "go":
            self.move()
        elif tokens[0] == "get":
            self.get_status()
        elif tokens[0] == "attack":
            self.attack()
        elif tokens[0] == "use":
            self.use_item()
        else:
            raise IOError

    def move(self):
        if len(self.tokens) > 2 or len(self.tokens) < 1:
            raise IOError
        else:
            old_location = self.player.getLocation().copy()
            self.player.move(self.tokens[1])
            new_location = self.level.getPosition(*self.player.getLocation())
            if not new_location.isPassable():
                print(f"You find yourself in {new_location.getDescription()}")
                print("You determine this route is impassable and return the way you came")
                self.player.setLocation(old_location)

    def get_status(self):
        if len(self.tokens) > 2:
            raise IOError
        elif len(self.tokens) == 2:
            _ = {
                "coords": self.player.getLocation(),
                "health": self.player.health,
                "inventory":self.player.getInventory(),
                "map":self.level.showMap()
            }
            if self.tokens[1] in _.keys():
                print(_[self.tokens[1]])
        else:
            raise IOError


    def player_turn(self):
        try:
            self.get_command()
        except IOError:
            print("something went wrong, try again")
            self.get_command()

    def use_item(self):
        try:
            if self.player.checkInventory(self.tokens[1]):
                item:Weapons = player.getItem(self.tokens[1])
                if isinstance(item, Weapons):
                    self.tokens.remove(self.tokens[1])
                    self.weapon = item.attack
                    self.attack()
                else:
                    raise IOError
            else:
                raise IOError
        except IndexError:
            raise IOError



def main(level=Level(),npcs=[]):
    print(disclaimer)
    player = setupPlayer()
    game = Game(player, npcs, level)
    game.gameLoop()
    
def setupPlayer()->Character:
    print("what is you name?:")
    player_name = input()
    return assignClass(player_name)

def assignClass(player_name)->Character:
    print("Please select your class. \nChoose either; Warior, Explorer or Scholar:")
    player_class = input()
    inventory = Inventory(6)
    if player_class in ("w","W","warior","Warior","WARIOR"):
        return Warior(player_name, inventory)
    elif player_class in ("e","E","explorer","Explorer","EXPLORER"):
        return Explorer(player_name, inventory)
    elif player_class in ("s","S","scholar","Scholar","SCHOLAR"):
        return Scholar(player_name, inventory)
    else:
        print("Something went wrong lets try again")
        assignClass(player_name)



if __name__ == "__main__":

    forest = Biome().new("You are in a Forest", True)
    
    l = [
        [Tile(forest),Tile(forest),Tile(forest)],
        [Tile(forest),Tile(forest),Tile(forest)],
        [Tile(forest),Tile(forest),Tile(forest)]
        ]
    level = Level().manual(l)

    gru = NPC("gru", Coordinates(1, 1),Inventory(3))
    npcs={
        gru.name:gru,
    }

    # main(level, npcs)

    player = Character("ant", Inventory(4))
    g = Game(player, npcs, level)
    g.gameLoop()
