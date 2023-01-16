from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.widget import Widget


class Obstacle(Widget):
    source = StringProperty()

    def __init__(self, lane, parent_width, speed, **kwargs):
        super().__init__(**kwargs)
        self.lane = lane
        self.speed = speed
        if self.speed < 0:
            self.x = parent_width  # sets start position negative speed | from left
        else:
            self.x = -self.width

    # moves vehicle 2 pixels to right or left
    def move(self):
        self.x += dp(self.speed)


class Vehicle(Obstacle):
    length = 1 / 8

    def __init__(self, lane, type, parent_width, speed, **kwargs):
        super().__init__(lane, parent_width, speed, **kwargs)
        self.source = f'img/{type}_left.png' if self.speed < 0 else f'img/{type}_right.png'


class Trunk(Obstacle):
    length = 1 / 5

    def holds(self, frog):
        holding = frog.x >= self.x and frog.right <= self.right
        return holding

    def __init__(self, lane, parent_width, speed, **kwargs):
        super().__init__(lane, parent_width, speed, **kwargs)
        self.source = 'img/Trunk.png'