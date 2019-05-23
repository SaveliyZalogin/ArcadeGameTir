import arcade
from math import sin, cos, pi
import random
import time

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
BULLET_KD = 30

background = arcade.load_texture("img/364.jpg")
heroTexture = arcade.load_texture("img/pushka2.png")
crossHairTexture = arcade.load_texture("img/cross.png")
enemiesTexture = arcade.load_texture("img/ter.png")
bulletTexture = arcade.load_texture("img/bullet.png")

def get_distance(hero1, hero2):
    return ((hero1.x - hero2.x) ** 2 + (hero1.y - hero2.y) ** 2) ** 0.5


class Enemies():
    def __init__(self):
        self.here = 0
        if self.here == 0:
            list_position = [(200, 155), (70, 463), (560, 230)]
            self.x, self.y = random.choice(list_position)

    def draw(self):
        if self.x == 200:
            arcade.draw_texture_rectangle(self.x, self.y, 70, 130, enemiesTexture)
            self.here = 1
        if self.x == 70:
            arcade.draw_texture_rectangle(self.x, self.y, 50, 110, enemiesTexture)
            self.here = 2
        if self.x == 560:
            arcade.draw_texture_rectangle(self.x, self.y, 70, 130, enemiesTexture)
            self.here = 3

class Crosshair():
    def __init__(self):
        self.x = 420
        self.y = 300
        self.r = 5

    def draw(self, color=arcade.color.WHITE):
        arcade.draw_texture_rectangle(self.x, self.y, 50, 50, crossHairTexture)
        #arcade.draw_circle_filled(self.x, self.y, self.r, color)

    # def move(self, x, y):
    #   self.x += x
    #  self.y += y


class Bullet():
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.speed = 12
        self.dx = dx
        self.dy = dy
        self.color = [10, 10, 10]
        self.distance_live = 30

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, 10, 10, bulletTexture)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.distance_live -= 1

    def is_removeble(self):
        out_x = not 0 < self.x < SCREEN_WIDTH
        out_y = not 0 < self.y < SCREEN_HEIGHT
        return out_x or out_y or self.distance_live <= 0

    def is_hit(self, hero):
        return get_distance(self, hero) <= hero.x


class Hero():
    def __init__(self, color=arcade.color.RED, size=30):
        self.x = 470
        self.y = 110
        self.dir = 0
        self.r = size
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)
        self.color = color
        self.bullet_kd = BULLET_KD

    def update(self):
        self.bullet_kd -= 1

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
        self.bullet_list = []
        self.crosshair = Crosshair()
        self.bullet_list = []
        self.enemi_list = []
        self.wait = time.clock()
        self.bulletsCount = 30
        self.reloadBuleetsCount = 90

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(450, 300, 900, 600, background)
        for enemy in self.enemi_list:
            enemy.draw()
        self.hero.draw()
        self.crosshair.draw()
        arcade.draw_text(self.get_bullets(), 100, 100, arcade.color.WHITE)
        for bullet in self.bullet_list:
            bullet.draw()

    def update(self, delta_time):
        self.hero.update()
        if random.randint(0, 1400) < 10:
            self.enemi_list.append(Enemies())
        for bullet in self.bullet_list:
            bullet.move()
            if bullet.is_removeble():
                self.bullet_list.remove(bullet)
                self.wait = 0
            for enemy in self.enemi_list:
                if bullet.is_hit(enemy):
                    self.bullet_list.remove(bullet)
                    self.enemi_list.remove(enemy)
                    # Enemies().here -= 1
    def get_bullets(self):
        text = "{}\n".format(self.bulletsCount) + \
               "{}".format(self.reloadBuleetsCount)
        return text

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
        # if len(self.bullet_list) <= 0:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.bulletsCount > 0 and self.hero.bullet_kd <= 0:
                self.hero.bullet_kd = BULLET_KD
                self.hero.set_dir(self.crosshair)
                self.bullet_list.append(Bullet(self.crosshair.x + 60,
                                               self.hero.y + 25,
                                               self.hero.dx,
                                               self.hero.dy))
                self.bulletsCount -= len(self.bullet_list)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.reloadBuleetsCount > 0:
                self.reloadBuleetsCount -= 30 - self.bulletsCount
                self.bulletsCount = 30

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
