"""Homework 3, Problem 3: predator, prey, and human simulation."""
import random
import matplotlib.pyplot as plt


class Island(object):
    """Represent a square island containing animals."""

    def __init__(self, n: int, prey_count: int = 0,
                 predator_count: int = 0, count_humans: int = 0) -> None:
        """Create an empty grid and place the initial animals."""
        if n <= 0 or min(prey_count, predator_count, count_humans) < 0:
            raise ValueError("Island size and animal counts must be valid")
        if prey_count + predator_count + count_humans > n * n:
            raise ValueError("Too many animals for the island")
        self.grid_size = n
        self.grid = []
        for i in range(n):
            self.grid.append([0] * n)
        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int) -> None:
        """Place prey, predators, and humans at random empty locations."""
        for animal_class, amount in [(Prey, prey_count),
                                     (Predator, predator_count),
                                     (Human, count_humans)]:
            count = 0
            while count < amount:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if not self.animal(x, y):
                    animal = animal_class(island=self, x=x, y=y)
                    self.register(animal)
                    count += 1

    def clear_all_moved_flags(self) -> None:
        """Allow all animals to move again at the next tick."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        """Return the width of the island."""
        return self.grid_size

    def register(self, animal: "Animal") -> None:
        """Place an animal at its current coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: "Animal") -> None:
        """Remove an animal from its current location."""
        self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int):
        """Return the animal at a position, or -1 if outside the grid."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        """Return the island grid as a string."""
        s = ""
        for j in range(self.grid_size - 1, -1, -1):
            for i in range(self.grid_size):
                if not self.grid[i][j]:
                    s += "{:<3s}".format(".")
                else:
                    s += "{:<3s}".format(str(self.grid[i][j]))
            s += "\n"
        return s

    def count_prey(self) -> int:
        """Return the number of prey currently on the island."""
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if isinstance(self.animal(x, y), Prey):
                    count += 1
        return count

    def count_predators(self) -> int:
        """Return the number of predators currently on the island."""
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if isinstance(self.animal(x, y), Predator):
                    count += 1
        return count

    def count_humans(self) -> int:
        """Return the number of humans currently on the island."""
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if isinstance(self.animal(x, y), Human):
                    count += 1
        return count


class Animal(object):
    """Represent an animal that can move and breed on the island."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "A") -> None:
        """Store the animal's island, coordinates, and display name."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self) -> tuple:
        """Return the current x and y coordinates."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the animal's display character."""
        return self.name

    def check_grid(self, type_looking_for: type = int):
        """Return the first neighboring location of the requested type, or 0."""
        offset = [(-1, 1), (0, 1), (1, 1), (-1, 0),
                  (1, 0), (-1, -1), (0, -1), (1, -1)]
        for dx, dy in offset:
            x = self.x + dx
            y = self.y + dy
            if not 0 <= x < self.island.size() or not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x, y)) == type_looking_for:
                return (x, y)
        return 0

    def move(self) -> None:
        """Move to the first empty neighboring cell if not already moved."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.island.remove(self)
                self.x = location[0]
                self.y = location[1]
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """Create an animal of the same class when the breeding clock expires."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                new_animal = self.__class__(self.island, x=location[0],
                                            y=location[1])
                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        """Reset the moved flag for the next tick."""
        self.moved = False


class Prey(Animal):
    """Represent prey that moves and breeds."""
    breed_time = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "O") -> None:
        """Initialize prey and its breeding clock."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Decrease the breeding clock by one tick."""
        self.breed_clock -= 1


class Predator(Animal):
    """Represent predators that eat prey, move, breed, and starve."""
    breed_time = 6
    starve_time = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "X") -> None:
        """Initialize the predator's breeding and starving clocks."""
        Animal.__init__(self, island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Update clocks and remove the predator if it starves."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Move onto adjacent prey, eat it, and reset the starving clock."""
        if not self.moved:
            location = self.check_grid(Prey)
            if location:
                self.island.remove(self.island.animal(location[0], location[1]))
                self.island.remove(self)
                self.x = location[0]
                self.y = location[1]
                self.island.register(self)
                self.starve_clock = self.starve_time
                self.moved = True


class Human(Animal):
    """Represent humans that hunt predators, move, breed, and starve."""
    breed_time = 8
    starve_time = 6
    hunt_time = 2

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "H") -> None:
        """Initialize the human's breeding, starving, and hunting clocks."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time
        self.hunt_clock = self.hunt_time

    def clock_tick(self) -> None:
        """Decrease clocks and remove the human if it starves."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        self.hunt_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def hunt(self) -> None:
        """Hunt adjacent predators only when the hunting clock expires."""
        if self.hunt_clock <= 0:
            self.hunt_clock = self.hunt_time
            if not self.moved:
                location = self.check_grid(Predator)
                if location:
                    self.island.remove(self.island.animal(location[0], location[1]))
                    self.island.remove(self)
                    self.x = location[0]
                    self.y = location[1]
                    self.island.register(self)
                    self.starve_clock = self.starve_time
                    self.moved = True


def main(predator_breed_time: int = 6, predator_starve_time: int = 3,
         initial_predators: int = 10, prey_breed_time: int = 3,
         initial_prey: int = 50, size: int = 10, ticks: int = 1000,
         human_breed_time: int = 8, human_starve_time: int = 6,
         human_hunt_time: int = 2, initial_humans: int = 5) -> None:
    """Run the simulation and plot all three animal populations."""
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    predator_list = []
    prey_list = []
    human_list = []
    isle = Island(size, initial_prey, initial_predators, initial_humans)

    print("Renato Zegarra")
    print("FAU ID: Z23342300")
    print("Homework 3 - Problem 3")
    print("Initial island:")
    print(isle)

    previous_counts = None
    unchanged_ticks = 0
    for i in range(min(ticks, 1000)):
        isle.clear_all_moved_flags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    if isinstance(animal, Predator):
                        animal.eat()
                    elif isinstance(animal, Human):
                        animal.hunt()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        prey_count = isle.count_prey()
        predator_count = isle.count_predators()
        human_count = isle.count_humans()
        prey_list.append(prey_count)
        predator_list.append(predator_count)
        human_list.append(human_count)
        counts = (prey_count, predator_count, human_count)
        if i % 10 == 0:
            print("Tick {}: Prey {}, Predators {}, Humans {}".format(
                i + 1, prey_count, predator_count, human_count))

        if counts == previous_counts:
            unchanged_ticks += 1
        else:
            unchanged_ticks = 0
        previous_counts = counts
        if unchanged_ticks >= 20:
            print("All populations remained constant for 20 ticks.")
            break

    print("Final island:")
    print(isle)
    print("Final populations: Prey {}, Predators {}, Humans {}".format(
        isle.count_prey(), isle.count_predators(), isle.count_humans()))

    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.xlabel("Time (ticks)")
    plt.ylabel("Population")
    plt.title("Predator-Prey-Human Simulation")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
