import arcade
import random
import timeit
from numpy import clip
from math import floor
import math


class FluidRenderer(arcade.Window):
    def __init__(self, size, window_size, fluid):
        self.size = size
        self.window_size = window_size
        self.fluid = fluid
        self.scale = window_size / (size * 2.05)

        self.frame_count = 0
        self.last_delta_time = 0

        self.window_width = window_size
        self.window_height = window_size

        super().__init__(self.window_width, self.window_height)

        arcade.set_background_color(arcade.color.AUROMETALSAURUS)

    def setup(self):
        pass

    def on_draw(self):
        draw_start_time = timeit.default_timer()

        arcade.start_render()
        arcade.set_background_color(arcade.color.AUROMETALSAURUS)

        self.frame_count += 1

        self.fluid.step()

        for particle in self.fluid.particles:
            position = particle.position

            arcade.draw_circle_filled((position.x * self.scale) + self.window_size / 2, (position.y * self.scale) +
                                      self.window_size / 2, 2, arcade.color.BLACK)

        draw_time = timeit.default_timer() - draw_start_time

        fps = 1.0 / draw_time

        arcade.draw_text("frame_count: %6d" % self.frame_count, 10, self.height - 14, arcade.color.BLACK, 12)
        arcade.draw_text("delta_time: %12.6f" % self.last_delta_time, 10, self.height - 32, arcade.color.BLACK, 12)
        arcade.draw_text("fps:       %12.6f" % fps, 10, self.height - 50, arcade.color.BLACK, 12)

    def update(self, delta_time):
        self.last_delta_time = delta_time
