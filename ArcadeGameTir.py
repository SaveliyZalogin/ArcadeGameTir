import arcade
from math import sin, cos, pi

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

background = arcade.load_texture("googimage1.jpg")
heroTexture = arcade.load_texture("goodimage2.jpg")

def get_distance(hero1, hero2):
    return ((hero1.x - hero2.x) ** 2 + (hero1.y - hero2.y) ** 2) ** 0.5


class Crosshair():
    def __init__(self):
        self.x = 450
        self.y = 300
        self.r = 5

    def draw(self, color = arcade.color.WHITE):
        arcade.draw_circle_filled(self.x, self.y, self.r, color)

    #def move(self, x, y):
    #   self.x += x
    #  self.y += y


class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.speed = 3
        self.dx = dx * self.speed
        self.dy = dy * self.speed
        self.color = [10, 10, 10]

    def draw(self):
        arcade.draw_line(self.x, self.y,
                         self.x + self.dx * 5,
                         self.y + self.dy * 5,
                         self.color, 4)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def is_removeble(self):
        out_x = not 0 < self.x < SCREEN_WIDTH
        out_y = not 0 < self.y < SCREEN_HEIGHT
        return out_x or out_y

    def is_hit(self, hero):
        return get_distance(self, hero) <= hero.r


class Hero():
    def __init__(self, color=arcade.color.RED, size=30):
        self.x = 450
        self.y = 150
        self.dir = 0
        self.r = size
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)
        self.color = color

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, 900, 300, heroTexture)
        #x1, y1, = self.x, self.y
        #x2 = x1 + self.r * 1.3 * self.dx
        #y2 = y1 + self.r * 1.3 * self.dy
        #arcade.draw_line(x1, y1, x2, y2, arcade.color.BLACK, 4)

    def turn_left(self):
        self.x -= 20

    def turn_right(self):
        self.x += 20


class MyGame(arcade.Window):
    def __init__(self, widht, height):
        super().__init__(widht, height)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.hero = Hero()
        self.bullet_list = []
        self.crosshair = Crosshair()

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
            self.hero.turn_left()
        #elif key == arcade.key.RIGHT:
        #   self.hero.turn_right()
        #elif key == arcade.key.SPACE:
        #    self.bullet_list.append(Bullet(self.hero.x + self.hero.dx * self.hero.r,
        #                                   self.hero.y + self.hero.dy * self.hero.r,
        #                                   self.hero.dx, self.hero.dy))

    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.x = x
        self.crosshair.y = y



def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()