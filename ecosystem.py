import random as r


class River:
    def __init__(self, size, bears, fish):
        self.river = [["🟦" for _ in range(size)] for _ in range(size)]
        self.size = size
        self.num_bears = bears
        self.num_fish = fish
        self.animals = []
        self.population = 0
        self.__initial_population()

    def __getitem__(self):
        return self.animals

    def __str__(self):
        riverStr = ""
        for i in range(self.size):
            for x in range(self.size):
                riverStr += f"{self.river[i][x]} "
            riverStr += "\n"
        return riverStr

    def __initial_population(self):
        # places num_bears and num_fish animals in the river
        for i in range(self.num_bears):
            self.place_baby("Bear")
        for i in range(self.num_fish):
            self.place_baby("Fish")

    def new_day(self):
        # day cycle
        # all animals move, add new babies at end of day
        babyList = []
        for i in self.animals:
            i.bred_today = False
            baby = i.move(self)
            if baby == "🐟":
                babyList.append("Fish")
            elif baby == "🐻":
                babyList.append("Bear")

        for i in babyList:
            self.place_baby(i)

        if self.num_bears == 0 or self.num_fish == 0:
            print("There are no more bears/fish!")
            return True

        return False
        pass

    def place_baby(self, baby):
        # place a new animal object in an open river tile
        # update population + animal
        y = r.randint(0, self.size - 1)
        x = r.randint(0, self.size - 1)
        if self.population < self.size * self.size:
            while self.river[y][x] != "🟦":
                x = r.randint(0, self.size - 1)
                y = r.randint(0, self.size - 1)
        else:
            print("Cannot place baby")
            return False

        if baby.capitalize() == "Bear":
            baby = Bear(x, y)
            self.num_bears += 1
            print("🐻 was born!")

        elif baby.capitalize() == "Fish":
            baby = Fish(x, y)
            self.num_fish += 1
            print("🐟 was born!")

        self.animals.append(baby)
        self.river[y][x] = baby
        self.population += 1

    def animal_death(self, animal):
        # remove a dead animal from the river
        # update population & animals
        self.river[animal.y][animal.x] = "🟦"

        if isinstance(animal, Bear):
            self.num_bears -= 1
        elif isinstance(animal, Fish):
            self.num_fish -= 1

        self.population -= 1

        pass

    def redraw_cells(self, oldX, oldY, animal):
        # update the river 2D array when an animal moves
        self.river[oldY][oldX] = "🟦"
        self.river[animal.y][animal.x] = animal


class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bred_today = False

    def death(self, river):
        # calls river’s death method - send the animal object
        print(f"{self} died")
        river.animal_death(self)

    def move(self, river):
        # randomly select a neighboring cell to move to in river bounds
        # calls River’s redraw cells & self.collision
        minX, minY = -1, -1
        maxX, maxY = 1, 1
        if self.x == 0:
            minX = 0
        elif self.y == 0:
            minY = 0
        elif self.x == (river.size - 1):
            maxX = 0
        elif self.y == (river.size - 1):
            maxY = 0
        oldX = self.x
        oldY = self.y
        self.x += r.randint(minX, maxX)
        self.y += r.randint(minY, maxY)
        # print(oldX, maxX, oldY, maxY)
        # print(self.x, self.y)
        baby = self.collision(river.river[self.y][self.x], river)
        if not baby:
            river.redraw_cells(oldX, oldY, self)
        else:
            self.bred_today = True
            self.x = oldX
            self.y = oldY

    def collision(self, other, river):
        # handles animal interactions
        # same=breed, different=consume
        if other == "🟦":
            return False
        ownType = type(self)
        otherType = type(other)
        if ownType == otherType:
            return str(self)  # adds it to the list of babies

        elif ownType != otherType:  # nom if bear & fish
            if ownType == Fish:
                other.consume(river, self)
            else:
                self.consume(river, other)


class Fish(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __str__(self):
        return "🐟"


class Bear(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.max_lives = 10
        self.lives = 0
        self.eaten_today = False

    def __str__(self):
        return "🐻"

    def starve(self, river):
        # increase lives if not eaten today
        # call death when 10
        self.lives += 1
        if self.lives == self.max_lives:
            self.death(river)

    def consume(self, river, fish):
        # consume a fish object
        # affects lives, causes fish death
        fish.death(river)
        self.lives -= 1
        
