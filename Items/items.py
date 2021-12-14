class Item:
    vsibility = 1
    def __init__(self,name):
        self.name = name
    def getVisibility(self, roll):
        if self.visibility == 1:
            return True
        elif self.visibility == 2:
            return  roll > 18
        else:
            return False

    def __repr__(self):
        return self.name


class Weapons(Item):
    def __init__(self, attack, name):
        self.attack = attack
        super(Weapons,self).__init__(name)


class Container(Item):
    pass


class Tool(Item):
    pass


class Consumable(Item):

    def __init__(self, trait, effect):
        self.trait = trait
        self.improvement = effect

    def use(self,target):
        traits = {
            "strength":target.strength,
            "speed":target.speed,
            "smarts":target.smarts,
            "visibility":target.visibility,
            "health":target.health
        }
        traits[self.trait] += self.improvement
        del self