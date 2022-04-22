
class Biome:

    def __init__(self):
        self.description = "You are in an undefined asset"
        self.passable = False

    def new(self, description:str, passable:bool):
        self.description = description
        self.passable = passable
        return self

    def isPassable(self)->bool:
        return self.passable

    def getDescription(self) -> str:
        return self.description


class Tile:

    def __init__(self,biome:Biome):
        self.biome = biome
        self.contents = []
        self.visible = []

    def update(self):
        self.visible = []
        for i in self.contents:
            if i.getVisibility():
                self.visible.append(i)

    def isPassable(self) -> bool:
        return self.biome.isPassable()

    def getDescription(self) -> str:
        return self.biome.getDescription()

    def __repr__(self) -> str:
        return f"{self.getDescription()}"
            

class Level:
    """ a Level can be instantiated 2 ways
    calling Level().new((int,int)) will randomly generate a Level
    calling Level().manual(2dArray) will turn a supplied 2d array into a level
    calling Level() does nothing useful
    """
    def __init__(self):
        self.level_map =[]
        self.size_x = 0
        self.size_y = 0

    def new(self, size:(int,int)):
        """Instanciates a Level of a given size
        note:
            the dimentions you supply are the number of tiles to extend outwards from coord 0,0. 
            so if you ran Level().new((0,0)) that would produce a map of 1 tile (located at 0,0)
            however if u ran Level().new((1,1)) it would create a level containing 9 tiles.
            (adding 1 tile in each direction.)
            """
        self.size_x, self.size_y = size
        for i in range((self.size_x * 2 + 1) * (self.size_y*2 + 1)):
            self.level_map.append(Tile(Biome()))
        return self
    
    def manual(self, array2d:list[list[Tile]]):
        """Will generate a level designed by the user. Level designs should be contained in a 2D array,
        where array2d[0][0] would be the southwestern corner of the map.
        """
        if isinstance(array2d, list) and isinstance(array2d[0], list) and isinstance(array2d[0][0], Tile):
            self.size_x = len(array2d[0])//2
            self.size_y = len(array2d)//2
            for i in array2d[::-1]:
                for x in i:
                    self.level_map.append(x)
            return self
        else:
            raise TypeError("the argument supplied to Level().manual(array2d) does not meet the required specifications.\nPlease fix this and try again.")

    def getPosition(self,x,y) ->Tile:
        "returns the information contained at a given coordinate"
        return self[x, y]

    def showMap(self)->list[list[Tile]]:
        width = self.size_x * 2 + 1
        height = self.size_y * 2 + 1
        out = []
        for i in range(0,len(self.level_map), width):
            out.append(self.level_map[i:i+width])
        return out

    def __iter__(self):
        for i in self.level_map:
            yield i

    def out_of_bounds(self, x, y)->bool:
        return not (-self.size_x < x < self.size_x or -self.size_y < y < self.size_y)

    def __getitem__(self,coord)->Tile:
        x = coord[0]
        y = coord[1]
        width = self.size_x * 2 + 1 
        middle = self.size_x + 1 + self.size_y + 1
        index = middle + x + (y * width)
        if middle * 2 >= index > 0 and x <= self.size_x and y <= self.size_y:
            return self.level_map[index]
        else:
            return Tile(Biome().new("A Dence Fog",False))



if __name__ == "__main__":
    print(Level().new((1,1)).showMap())