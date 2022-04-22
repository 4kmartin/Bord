class Item:
    
    def __init__(self,name):
        self.name = name
        self.usable = True
        self.visibility = 1
        self.weildable = True

    def setVisibility(self, number:int):
        """number must be between 1,2,3
        1 = easily seen
        2 = difficult to see
        3 = impossible to see
        """
        if 0 < number < 4:
            self.visibility = number
        else:
            raise ValueError("%s visibility cannot be set to %s" % (self.name, number))


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

    def __init__(self, attack:int, name:str):
        self.attack = attack
        super().__init__(name)


class Container(Item):
    
    def __init__(self, name:str, contents: list[Item], location):
        super().__init__(name)
        self.contents = contents
        self.location = location
        self.weildable = False


class Consumable(Item):

    def __init__(self, trait:str, effect:int):
        if traits not in ["strength","speed","smarts","visibility","health"]:
            raise ValueError("%s is not a valid Trait")
        self.trait = trait
        self.improvement = effect

    def use(self):
        self.usable = False
        return self.trait, self.int


class Inventory:

    def __init__(self, slots: int):
        self.contents:dict[Item] = {}
        self.inventory_size = slots

    def update(self):
        if len(self.contents) > self.inventory_size:
            self.contents.clear()
            print("You overfilled your inventory and lost everything")
        for item in self.contents.items():
            if not item.usable:
                self.contents.remove(item)

    def addItem(self, item:Item):
        self.contents.append(item)
        self.update()

    def keys(self):
        return self.contents.keys()

    def __getitem__(self,key):
        return self.contents[key]        

    def __repr__(self) ->str:
        inventory = ""
        for item in self.contents:
            inventory += "{item}"

        return inventory
        

class LootTable:

    def __init__(self, loot:list[Item], rarity: list[int]):
        self.table = []
        if len(loot) != len(rarity):
            raise ValueError("not all loot items have a corresponding rarity value")
        for i in range(len(loot)):
            for _ in range(rarity[i]):
                self.table.append(loot[i])
        for _ in range(10):
            self.table.append[None]

    def fill_container(self, max_items:int) -> list[Item]:
        contents = []
        for _ in range(max_items):
            item = random.choice(self.table)
            if item is None:
                continue
            else:
                contents.append(item)
        

