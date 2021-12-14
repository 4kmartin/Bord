

class Level:
    level_map =[[]]

    def new(self, size:list):
        """Instanciates a 2d Vector of a given size"""
        self.level_map = []
        for i in range(size[0]):
            x = []
            for _ in range(size[1]):
                x.append(Tile())
            self.level_map.append(x)
    
    def manual(self, array2d):
        self.level_map = array2d
        return self

    def __iter__(self):
        for i in self.level_map:
            for x in i:
                yield x


class Biome:
   description = "You are in an undefined asset"
   passable = False


class Tile:

    visible = []

    def __init__(self, contents = [], biome = Biome()):
        self.biome = biome
        self.contents = contents

    def update(self):
        self.visible = []
        for i in self.contents:
            if i.getVisibility():
                self.visible.append(i)
            
