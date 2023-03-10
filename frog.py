import kivy.metrics
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.metrics import dp
from direction import Direction


class Frog(Widget):
    lane = NumericProperty(0)

    def on_lane(self, *args):
        self.y = self.lane * self.parent.height / 14 + 4

    def jump(self, direction):  # moves our frog when in border
        height = self.parent.height
        width = self.parent.width
        if direction == Direction.FORWARD and height - height / 14 >= self.y:  # checks if jump is in window/border
            self.lane += 1
        if direction == Direction.BACKWARD and 0 + height / 14 <= self.y:
            self.lane -= 1
        if direction == Direction.RIGHT and width > self.x + self.width:
            self.x += self.width
        if direction == Direction.LEFT and 0 <= self.x:
            self.x -= self.width
        if self.y > height - height / 14:
            self.reset()
            self.parent.score += 1

    def move(self, speed):
        self.x += dp(speed)

    # resets frog to starting position
    def reset(self):
        self.lane = 0
        self.center_x = self.parent.width / 2
