import arcade
from arcade import Texture
import math
import random
import time
import os

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720

background = arcade.load_texture("img/364.jpg")
heroTexture = arcade.load_texture("img/pushka2.png")
crossHairTexture = arcade.load_texture("img/cross.png")
enemiesTexture = arcade.load_texture("img/ter.png")
bulletTexture = arcade.load_texture("img/bullet.png")

PRIMARY_GUN = 0
SECONDARY_GUN = 1

VIEWPORT_MARGIN = SCREEN_WIDTH // 2 + 100


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures = []
        texture = arcade.load_texture("img/pushka2.png")
        self.textures.append(texture)
        texture = arcade.load_texture("img/handsWithGun2.png")
        self.textures.append(texture)
        self.set_texture(PRIMARY_GUN)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game v2.0')
        self.set_mouse_visible(False)
        self.cooldown = False
        self.counter = 0
        self.primary = False
        self.secondary = False
        self.crosshair_list = None
        self.hero_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.score = 0
        self.center = 175
        self.bullet_x = -30
        self.bullet_y = 50
        self.is_secondary = False
        self.hit_position = ()
        self.position_list = [(100, 600), (300, 200), (600, 400), (900, 300)]
        self.position_unfree = []
        self.view_bottom = 0
        self.view_left = 0
        self.changed = False

    def setup(self):
        self.crosshair_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.hero_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.hero_sprite = Hero()
        self.hero_sprite.center_x = 512 + self.center
        self.hero_sprite.center_y = 110
        self.hero_list.append(self.hero_sprite)

        self.crosshair = arcade.Sprite("img/cross.png", .3)
        self.crosshair.center_x = 450
        self.crosshair.center_y = 360
        self.crosshair_list.append(self.crosshair)

        self.view_bottom = 0
        self.view_left = 0

    def on_draw(self):
        arcade.start_render()
        #all scene width = 2048
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2 + 40, SCREEN_HEIGHT // 2, SCREEN_WIDTH * 2, SCREEN_HEIGHT, background)
        self.enemy_list.draw()
        self.crosshair_list.draw()
        self.bullet_list.draw()
        self.hero_list.draw()
        arcade.draw_text(f'Score: {self.score}', 10, 10, arcade.color.WHITE, 20)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.hero_sprite.center_x = x + self.center
        self.crosshair.center_x = x
        self.crosshair.center_y = y

    def on_update(self, delta_time):
        self.bullet_list.update()
        self.position = random.choice(self. position_list)
        if self.is_secondary:
            self.counter += 2
        else:
            self.counter += 1
        if self.counter == 60:
            self.cooldown = True
            self.counter = 0

        if random.randint(0, 1200) < 10:
            if self.position not in self.position_unfree:
                self.enemy_sprite = arcade.Sprite("img/ter.png", .3)
                self.enemy_sprite.center_x = self.position[0]
                self.enemy_sprite.center_y = self.position[1]
                self.enemy_list.append(self.enemy_sprite)
                self.position_unfree.append((self.position[0], self.position[1]))

        distance_list = arcade.check_for_collision_with_list(self.crosshair, self.bullet_list)
        if len(distance_list) > 0:
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    self.position_unfree.remove((enemy.center_x, enemy.center_y))
                    self.score += 1

                if bullet.top >= SCREEN_HEIGHT or bullet.left <= 0:
                    self.bullet_list.remove(bullet)
                if len(hit_list) > 0:
                    self.bullet_list.remove(bullet)

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.crosshair.left < left_boundary:
            self.view_left -= left_boundary - self.crosshair.left
            self.changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.crosshair.right - 100 > right_boundary:
            self.view_left += self.crosshair.right - 100 - right_boundary
            self.changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        if self.changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
            self.changed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.cooldown == True:
            bullet = arcade.Sprite("img/bullet2.png", .08)
            start_x = self.hero_sprite.center_x
            start_y = self.hero_sprite.center_y
            bullet.center_x = start_x + self.bullet_x
            bullet.center_y = start_y + self.bullet_y

            dest_x = x
            dest_y = y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            bullet.angle = math.degrees(angle)
            print(f"Bullet angle: {bullet.angle:.2f}")

            bullet.change_x = math.cos(angle) * 5
            bullet.change_y = math.sin(angle) * 5
            self.bullet_list.append(bullet)
            self.cooldown = False

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.KEY_1:
            self.hero_sprite.set_texture(PRIMARY_GUN)
            self.counter = 0
            if self.is_secondary:
                self.center -= 150
                self.bullet_x += 70
                self.is_secondary = False
        elif key == arcade.key.KEY_2:
            self.hero_sprite.set_texture(SECONDARY_GUN)
            if self.is_secondary == False:
                self.counter = 30
                self.bullet_x -= 70
                self.center += 150
                self.is_secondary = True



def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
