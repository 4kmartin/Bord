class Coordinates:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, vector:tuple[int]):
        self.x += vector[0]
        self.y += vector[1]

    def copy(self):
        return Coordinates(self.x, self.y)

    def __add__(self,vector:tuple[int])->tuple[int]:
        return (self.x + vector[0], self.y + vector[1])

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"(x:{self.x} y:{self.y})"


class Character:

    def __init__(self,name: str, inventory):
        self.name = name
        self.strength = 1
        self.smarts = 1
        self.speed = 1
        self.inventory = inventory
        self.health = 100
        self.visibility = 1
        self.location = Coordinates(0, 0)

    def hit(self, roll:int, weapon:int = 0):
        return self.strength + roll + weapon

    def dodge(self, roll:int):
        # enables a player to take less damage
        return self.speed + roll
    
    def hide(self, roll:int):
        if roll + smarts > 18:
            self.visibility += 1
        else:
            self.visibility = 1

    def getLocation(self)->Coordinates:
        return self.location
    
    def setLocation(self, new_location):
        self.location = Coordinates(*new_location)

    def move(self, direction:str):
        directions ={
            "north": (0,1),
            "east": (1,0),
            "south": (0,-1),
            "west": (-1,0)
        }
        try:
            vector = directions[direction.lower()]
            self.location.translate(vector)
        except KeyError:
            raise IOError
    

    def getVisibility(self, roll):
        if self.visibility == 1:
            return True
        elif self.visibility == 2:
            return  roll > 18
        else:
            return False

    def getItem(self, item_name:str) :
        return self.inventory[item_name]

    def checkInventory(self, item_name) -> bool:
        return item_name in self.inventory.keys()


class Warior(Character):
    
    def __init__(self,name, inventory):
        super().__init__(name, inventory)
        self.strength = 3

    def hit(self, roll:int, weapon = 0):
        # warior has a 25% chance to Critical hit
        if roll > 15:
            return 100
        else:
            return self.strength + roll + weapon            


class Explorer(Character):
    

    def __init__(self,name,inventory):
        super().__init__(name,inventory)
        self.speed = 3


class Scholar(Character):

    def __init__(self,name,inventory):
        super().__init__(name,inventory)
        self.smarts = 3


class NPC(Character):
    
    def __init__(self, name, start_location:Coordinates,inventory):
        super().__init__(name,inventory)
        self.location = start_location

    def turn(self, player:Character, roll:int):
        if player.location == self.location and player.getVisibility(roll):
            hit = self.hit(roll)
            player.health -= hit
            print("You were hit by a %s for %s points, your health is now %s/100" % (self.name,hit,player.health))
        

