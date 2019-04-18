import arcade
from math import sin, cos, pi
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

background = arcade.load_texture("img/364.jpg")
heroTexture = arcade.load_texture("img/pushka2.png")
crossHairTexture = arcade.load_texture("img/cross.png")
# enemiesTexture = arcade.load_texture("")


def get_distance(hero1, hero2):
    return ((hero1.x - hero2.x) ** 2 + (hero1.y - hero2.y) ** 2) ** 0.5


class Enemies():
    def __init__(self):
        self.x = random.randint(0, 900)
        self.y = random.randint(0, 600)

    def draw(self):
        pass

class Crosshair():
    def __init__(self):
        self.x = 420
        self.y = 300
        self.r = 5

    def draw(self, color=arcade.color.WHITE):
        arcade.draw_texture_rectangle(self.x, self.y, 50, 50, crossHairTexture)
        #arcade.draw_circle_filled(self.x, self.y, self.r, colo

    # def move(self, x, y):
    #   self.x += x
    #  self.y += y


class Bullet():
    def __init__(self, x, y, dx, dy, distance_live=1000):
        self.x = x
        self.y = y
        self.speed = 3
        self.dx = dx
        self.dy = dy
        self.color = [10, 10, 10]
        self.distance_live = distance_live

        # self.crosshair = Crosshair()

    def draw(self):
        arcade.draw_line(self.x, self.y,
                         self.x + self.dx * 5,
                         self.y + self.dy * 5,
                         self.color, 4)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.distance_live -= (self.dy * self.speed ** 2 + self.dx * self.speed ** 2) ** 0.5

    def is_removeble(self):
        out_x = not 0 < self.x < SCREEN_WIDTH
        out_y = not 0 < self.y < SCREEN_HEIGHT
        return out_x or out_y or self.distance_live <= 0

    def is_hit(self, hero):
        return get_distance(self, hero) <= hero.r


class Hero():
    def __init__(self, color=arcade.color.RED, size=30):
        self.x = 470
        self.y = 110
        self.dir = 0
        self.r = size
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)
        self.color = color

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, 450, 220, heroTexture)

    def turn_left(self):
        self.x -= 20

    def turn_right(self):
        self.x += 20

    def set_dir(self, cross):
        dx = cross.x - self.x
        dy = cross.y - self.y
        r = (dx ** 2 + dy ** 2) ** 0.5
        self.dx = dx / r
        self.dy = dy / r


class MyGame(arcade.Window):
    def __init__(self, widht, height):
        super().__init__(widht, height)
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.hero = Hero()
        self.crosshair = Crosshair()
        self.bullet_list = []
        # self.bullet = Bullet

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(450, 300, 900, 600, background)
        self.hero.draw()
        self.crosshair.draw()
        for bullet in self.bullet_list:
            bullet.draw()

    def update(self, delta_time):
        for bullet in self.bullet_list:
            bullet.move()
            if bullet.is_removeble():
                self.bullet_list.remove(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            pass
            # self.hero.turn_left()
        #elif key == arcade.key.RIGHT:
        #   self.hero.turn_right()
        #elif key == arcade.key.SPACE:
        #
    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.x = x
        self.crosshair.y = y
        self.hero.x = x + 90
        # self.bullet.x = x
        # self.bullet.y = y

    def on_mouse_press(self, x: float, y: float, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.hero.set_dir(self.crosshair)
            self.bullet_list.append(Bullet(self.crosshair.x + 60,
                                            self.hero.y + 25,
                                            self.hero.dx,
                                            self.hero.dy))


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
