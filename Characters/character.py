class Character:
    strength = 1
    smarts = 1
    speed = 1
    items = {}
    health = 100
    visibility = 1
    location = [0,0]
    def __init__(self,name):
        self.name = name

    def hit(self, roll, weapon = 0):
        return self.strength + roll + weapon

    def dodge(self, roll):
        # enables a player to take less damage
        return self.speed + roll
    
    def hide(self, roll):
        if roll + smarts > 18:
            self.visibility += 1
        else:
            self.visibility = 1

    def move(self, direction):
        old = self.location.copy()
        if direction == "north":
            self.location[0]+=1
        elif direction == "south":
            self.location[0] -= 1 * self.location[0]-1>=0
        elif direction == "east":
            self.location[1]+=1
        elif direction == "west":
            self.location[1] -= 1 * self.location[1]-1>=0
        else: 
            raise IOError
        if old == self.location:
            print("You can't go that way")


    def getVisibility(self, roll):
        if self.visibility == 1:
            return True
        elif self.visibility == 2:
            return  roll > 18
        else:
            return False


class Warior(Character):
    strength = 3

    def __init__(self,name):
        super(Warior, self).__init__(name)
    
    def hit(self, roll, weapon = 0):
        # warior has a 25% chance to Critical hit
        if roll > 15:
            return 100
        else:
            return self.strength + roll + weapon            


class Explorer(Character):
    speed = 3

    def __init__(self,name):
        super(Explorer, self).__init__(name)


class Scholar(Character):
    smarts = 3

    def __init__(self,name):
        super(Scholar, self).__init__(name)


class NPC(Character):
    
    def __init__(self, name, start_location):
        self.location = start_location
        super(NPC,self).__init__(name)

    def turn(self, player:Character, roll):
        if player.location == self.location and player.getVisibility(roll):
            hit = self.hit(roll)
            player.health -= hit
            print("You were hit by a %s for %s points, your health is now %s/100" % (self.name,hit,player.health))
        if self.health < 1:
            del self

