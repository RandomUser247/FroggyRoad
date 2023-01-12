from random import randint

from kivy.uix.widget import Widget

from Obstacle import Vehicle, Trunk


class Lane(Widget):
    def __init__(self, speed, cycle, number, **kwargs):
        super().__init__(**kwargs)
        self.obstacles = []
        self.speed = speed
        self.cycle = cycle
        self.number = number
        self.cycle_counter = 120
        self.variance = 50

    def _spawn(self, obstacle):
        self.obstacles.append(obstacle)  # sets vehicles on random lane
        self.parent.add_widget(self.obstacles[-1], 1001)  # adding vehicles to app
        obstacle.width = self.parent.height * obstacle.length
        obstacle.height = self.parent.height / 14 - 4
        obstacle.y = self.obstacles[-1].lane * self.parent.height / 14 + 4

class RiverLane(Lane):
    def spawn(self):
        # counts up to value of cycle (example 120 cycles(2sec)), after spawns an obstacle and resets counter
        if self.cycle_counter >= self.cycle and randint(0, 50) == 0:
            new_obstacle = Trunk(self.number, self.parent.width, self.speed)
            Lane._spawn(self, new_obstacle)
            self.cycle_counter = 0
        else:
            self.cycle_counter += 1

    def is_on_Trunk(self, frog):
        return any([obstacle.holds(frog) for obstacle in self.obstacles])

class RoadLane(Lane):
    def __init__(self, speed, cycle, number, vehicle_type, **kwargs):
        super().__init__(speed, cycle, number, **kwargs)
        self.vehicle_type = vehicle_type
        self.variance = 90

    def spawn(self):
        if self.cycle_counter >= self.cycle and randint(0, self.variance) == 0:
            new_obstacle = Vehicle(self.number, self.vehicle_type, self.parent.width, self.speed)
            Lane._spawn(self, new_obstacle)
            self.cycle_counter = 0
        else:
            self.cycle_counter += 1