# import libraries
from time import sleep

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget

from Lane import RiverLane, RoadLane
from Obstacle import Vehicle, Trunk
from direction import Direction
# noinspection PyUnresolvedReferences
from frog import Frog


# class handles game logic and widgets
class FroggerGame(Widget):
    frog = ObjectProperty(None)  # to handle our frog through frogger.kv
    game_time = NumericProperty(0)
    score = NumericProperty(0)  # keeps track of the player score

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # need to open init super function (from Widget) to extend it
        self.down = False  # blocker for keyboard down
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self)  # connects our app with kivy keyboard to listen to keyboard events
        self._keyboard.bind(on_key_down=self._on_keyboard_down)  # binds our function to widget function
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.timer_counter = 0
        self.lanes = [RoadLane(speed=-3, cycle=120, number=1, vehicle_type='Station_wagon'),
                      RoadLane(speed=2, cycle=200, number=2, vehicle_type='Truck'),
                      RoadLane(speed=-3, cycle=250, number=3, vehicle_type='Convertible'),
                      RoadLane(speed=-4, cycle=200, number=4, vehicle_type='Convertible'),
                      RoadLane(speed=15, cycle=180, number=5, vehicle_type='Truck'),
                      RoadLane(speed=-2, cycle=120, number=6, vehicle_type='Truck'),
                      RiverLane(speed=1, cycle=250, number=8),
                      RiverLane(speed=-1, cycle=500, number=9),
                      RiverLane(speed=1, cycle=300, number=10),
                      RiverLane(speed=-1, cycle=350, number=11),
                      RiverLane(speed=1, cycle=200, number=12)]
        for lane in self.lanes:
            self.add_widget(lane)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_up(self, *args):
        self.down = False  # sets blocker variable back to false on button release

    # gets first keyboard event and ignores following events until the button is released
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.down:  # blocks function until button release
            return
        self.down = True
        # calls function corresponding to keycode // keycode consists nummer- and string code for keyboard event
        match keycode[1]:
            case 'w' | 'up':
                self.frog.jump(Direction.FORWARD)
            case 's' | 'down':
                self.frog.jump(Direction.BACKWARD)
            case 'a' | 'left':
                self.frog.jump(Direction.LEFT)
            case 'd' | 'right':
                self.frog.jump(Direction.RIGHT)
        return True

    # gets called on app start
    def on_kv_post(self, base_widget):
        Window.size = (512, 512)

    # gets called when window.size changes
    def on_size(self, *args):
        for lane in self.lanes:
            for obstacle in lane.obstacles:  # changes position and size of vehicles depending on window size

                obstacle.width = self.height / 8 - 4 if isinstance(obstacle, Vehicle) else self.height / 5 - 4
                obstacle.height = self.height / 14 - 4
                obstacle.y = obstacle.lane * self.height / 14 + 4

    # reacts on swipe input and controls the frogs movement
    def on_touch_up(self, touch):
        if touch.dpos[1] > 0:
            self.frog.jump(Direction.FORWARD)
        elif touch.dpos[1] < 0:
            self.frog.jump(Direction.BACKWARD)
        elif touch.dpos[0] > 0:
            self.frog.jump(Direction.RIGHT)
        elif touch.dpos[0] < 0:
            self.frog.jump(Direction.LEFT)
        else:  # if touch has no swipe (like a click) frog jumps forward
            self.frog.jump(Direction.FORWARD)

    # gets called 60 times a second
    def update(self, dt):
        if self.timer_counter == 6:
            self.game_time += 1
            self.timer_counter = 0
        else:
            self.timer_counter += 1
        for lane in self.lanes:  # calls spawn function from every lane
            lane.spawn()
        frog_on_trunk = False
        for lane in self.lanes:
            if isinstance(lane, RiverLane) and self.frog.lane == lane.number and lane.is_on_Trunk(self.frog):
                self.frog.move(lane.speed)
                frog_on_trunk = True
            for obstacle in lane.obstacles:
                obstacle.move()  # moves every obstacle
                # sets back frog after a collision
                if obstacle.collide_widget(self.frog) and isinstance(obstacle, Vehicle):
                    self.frog.reset()
                    self.decrement_score()
                # removes vehicles out window from list and app
                if obstacle.right < - obstacle.width or obstacle.x > self.width + obstacle.width:
                    lane.obstacles.remove(obstacle)
                    self.remove_widget(obstacle)

        if not frog_on_trunk and self.frog.lane > 7:
            self.frog.reset()
            self.decrement_score()

    def decrement_score(self):
        if self.score > 0:
            self.score -= 1


# runs the app
class FroggerApp(App):
    def build(self):
        game = FroggerGame()
        Clock.schedule_interval(game.update, 1 / 60)  # calls update every intervall (60 times per second)
        return game


if __name__ == '__main__':
    FroggerApp().run()
