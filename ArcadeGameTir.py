import arcade
from arcade import Texture
from math import sin, cos, pi
import random
import time

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

background = arcade.load_texture("img/364.jpg")
heroTexture = arcade.load_texture("img/pushka2.png")
crossHairTexture = arcade.load_texture("img/cross.png")
enemiesTexture = arcade.load_texture("img/ter.png")
bulletTexture = arcade.load_texture("img/bullet.png")


def get_distance(hero1, hero2):
    return ((hero1.x - hero2.x) ** 2 + (hero1.y - hero2.y) ** 2) ** 0.5


class Enemies(arcade.Sprite):
    def __init__(self, texture):
        super().__init__()

    def position(self):
        list_position = [(200, 155), (70, 463), (560, 230)]
        self.center_x, self.center_y = random.choice(list_position)
        return self.center_x, self.center_y

    # def draw(self):
    #     arcade.draw_texture_rectangle(self.x, self.y, 70, 30, enemiesTexture)


class Crosshair(arcade.Sprite):
    def __init__(self, texture):
        super().__init__()
        self.x = 420
        self.y = 300
        self.r = 5

        #arcade.draw_circle_filled(self.x, self.y, self.r, color)

    # def move(self, x, y):
    #   self.x += x
    #  self.y += y


class Bullet(arcade.Sprite):
    def __init__(self, texture, x, y, dx, dy):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 12
        self.dx = dx
        self.dy = dy
        self.color = [10, 10, 10]
        self.distance_live = 25

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, 10, 10, bulletTexture)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.distance_live -= 1

    # def is_removeble(self):
    #     out_x = not 0 < self.x < SCREEN_WIDTH
    #     out_y = not 0 < self.y < SCREEN_HEIGHT
    #     return out_x or out_y or self.distance_live <= 0

    # def is_hit(self, bullet):
    #     return get_distance(self, bullet) <= bullet.x and get_distance(self, bullet) <= bullet.y


class Hero(arcade.Sprite):
    def __init__(self, color=arcade.color.RED, size=30):
        super().__init__()
        self.x = 470
        self.y = 110
        self.dir = 0
        self.r = size
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)
        self.color = color
        self.KD = 45
        self.killcount = 0

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, 450, 220, heroTexture)

    # def turn_left(self):
    #     self.x -= 20
    #
    # def turn_right(self):
    #     self.x += 20
    #
    # def set_dir(self, cross):
    #     dx = cross.x - self.x
    #     dy = cross.y - self.y
    #     r = (dx ** 2 + dy ** 2) ** 0.5
    #     self.dx = dx / r
    #     self.dy = dy / r


class MyGame(arcade.Window):
    def __init__(self, widht, height):
        super().__init__(widht, height)
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLACK)
        self.mouse_left_clicked = False
        self.hero_sprite = None
        self.bullet_list = None
        self.crosshair_list = None
        self.enemi_list = None
        self.wait = time.clock()
        self.bulletsCount = 30
        self.reloadBuleetsCount = 90

    def setup(self):
        self.hero_sprite = arcade.SpriteList()
        self.hero = Hero(heroTexture)
        self.hero.center_x = 470
        self.hero.center_y = 110
        self.hero.width = 450
        self.hero.height = 220
        self.hero_sprite.append(self.hero)

        self.bullet_list = arcade.SpriteList()

        self.crosshair_list = arcade.SpriteList()
        self.crosshair = Crosshair(crossHairTexture)
        self.crosshair.center_x = SCREEN_WIDTH // 2
        self.crosshair.center_y = SCREEN_HEIGHT // 2
        self.crosshair.width = 50
        self.crosshair.height = 50
        self.crosshair_list.append(self.crosshair)

        self.enemi_list = arcade.SpriteList()
        self.enemy = Enemies(enemiesTexture)
        self.enemy.center_x = self.enemy.position()
        self.enemy.center_y = self.enemy.position()
        self.enemy.width = 35
        self.enemy.height = 80

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(450, 300, 900, 600, background)
        self.hero_sprite.draw()
        self.bullet_list.draw()
        # for enemy in self.enemi_list:
        #     enemy.draw()
        # self.hero.draw()
        # self.crosshair.draw()
        # arcade.draw_text(self.kill_count(), 150, 100, arcade.color.WHITE)
        # arcade.draw_text(self.get_bullets(), 100, 100, arcade.color.WHITE)
        # for bullet in self.bullet_list:
        #     bullet.draw()

    def update(self, delta_time):
        if random.randint(0, 1200) < 10:
            self.enemi_list.append(self.enemy)

        for bullet in self.bullet_list:
            bullet.move()

        hit_list = arcade.check_for_collision_with_list(self.enemy, self.bullet_list)
        for enemy in hit_list:
            enemy.remove_from_sprite_lists()
        for bullet in hit_list:
            bullet.remove_from_sprite_lists()
            # if bullet.is_removeble():
            #     self.bullet_list.remove(bullet)
            # for enemy in self.enemi_list:
            #     if bullet.is_hit(enemy):
            #         self.bullet_list.remove(bullet)
            #         self.enemi_list.remove(enemy)
            #         self.hero.killcount += 1

    def kill_count(self):
        killtext = "{}\n".format(self.hero.killcount)
        return killtext

    def get_bullets(self):
        text = "{}\n".format(self.bulletsCount) + \
               "{}".format(self.reloadBuleetsCount)
        return text

    def on_key_press(self, key, modifiers):
       pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.x = x
        self.crosshair.y = y
        self.hero.x = x + 90
        # self.bullet.x = x
        # self.bullet.y = y

    def on_mouse_press(self, x: float, y: float, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_left_clicked = True
            if self.bulletsCount > 0:
                    self.bullet_list.append(Bullet(bulletTexture, self.crosshair.center_x + 60,
                                                    self.hero.center_y + 25,
                                                    self.hero.dx,
                                                    self.hero.dy))
                    self.bulletsCount -= len(self.bullet_list)
                    self.hero.KD += 45
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.reloadBuleetsCount > 0:
                self.reloadBuleetsCount -= 30 - self.bulletsCount
                self.bulletsCount = 30

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_left_clicked = False

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
