import arcade
from math import sin, cos, pi
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

background = arcade.load_texture("img/364.jpg")
heroTexture = arcade.load_texture("img/pushka.png")
crossHairTexture = arcade.load_texture("img/cross.png")
enemiesTexture = arcade.load_texture("img/ter.png")


def get_distance(hero1, hero2):
    return ((hero1.x - hero2.x) ** 2 + (hero1.y - hero2.y) ** 2) ** 0.5


class Enemies():
    def __init__(self):
        list_position = [(200, 155), (70, 463), (560, 230)]
        self.x, self.y = random.choice(list_position)

    def draw(self):
        if self.x == 200:
            arcade.draw_texture_rectangle(self.x, self.y, 90, 150, enemiesTexture)

        if self.x == 70:
            arcade.draw_texture_rectangle(self.x, self.y, 50, 110, enemiesTexture)

        if self.x == 560:
            arcade.draw_texture_rectangle(self.x, self.y, 70, 130, enemiesTexture)
class Crosshair():
    def __init__(self):
        self.x = 450
        self.y = 300
        self.r = 5

    def draw(self, color=arcade.color.WHITE):
        arcade.draw_texture_rectangle(self.x, self.y, 50, 50, crossHairTexture)
        #arcade.draw_circle_filled(self.x, self.y, self.r, color)

    # def move(self, x, y):
    #   self.x += x
    #  self.y += y


class Bullet:
    def __init__(self, x, y, dx, dy, distance_live=100):
        self.x = x
        self.y = y
        self.speed = 3
        self.dx = dx * self.speed
        self.dy = dy * self.speed
        self.color = [10, 10, 10]
        self.distance_live = distance_live

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
        self.x = 200
        self.y = 63
        self.dir = 0
        self.r = size
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)
        self.color = color

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, 350, 250, heroTexture)
        #x1, y1, = self.x, self.y
        #x2 = x1 + self.r * 1.3 * self.dx
        #y2 = y1 + self.r * 1.3 * self.dy
        #arcade.draw_line(x1, y1, x2, y2, arcade.color.BLACK


    def turn_left(self):
        self.x -= 20

    def turn_right(self):
        self.x += 20


class MyGame(arcade.Window):
    def __init__(self, widht, height):
        super().__init__(widht, height)
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.hero = Hero()
        self.bullet_list = []
        self.crosshair = Crosshair()
        self.enemi_list = []

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(450, 300, 900, 600, background)
        for enemy in self.enemi_list:
            enemy.draw()
        self.hero.draw()
        self.crosshair.draw()
        for bullet in self.bullet_list:
            bullet.draw()

    def update(self, delta_time):
        if random.randint(0, 1400) < 10:
            self.enemi_list.append(Enemies())

        for bullet in self.bullet_list:
            bullet.move()
            if bullet.is_removeble():
                self.bullet_list.remove(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.hero.turn_left()

    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.x = x
        self.crosshair.y = y
        self.hero.x = x

    def on_mouse_press(self, x: float, y: float, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.bullet_list.append(Bullet(self.hero.x + self.hero.dx * self.hero.r,
                                               self.hero.y + self.hero.dy * self.hero.r,
                                               self.hero.dx, self.hero.dy))


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
