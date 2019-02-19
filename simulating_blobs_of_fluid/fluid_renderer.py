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

        self.fluid.dt = self.last_delta_time
        self.fluid.step()

        radius = self.fluid.iteraction_radius * self.scale
        influence_radius = self.fluid.iteraction_radius_size * self.scale

        for particle in self.fluid.particles:
            position = particle.position
            old_position = particle.old_postion

            pos_x = (position.x * self.scale) + self.window_size / 2
            pos_y = (position.y * self.scale) + self.window_size / 2

            old_pos_x = (old_position.x * self.scale) + self.window_size / 2
            old_pos_y = (old_position.y * self.scale) + self.window_size / 2

            arcade.draw_line(pos_x, pos_y, old_pos_x, old_pos_y, arcade.color.ORANGE_RED, 2)
            arcade.draw_circle_filled(pos_x, pos_y, radius, arcade.color.BLACK)
            arcade.draw_circle_outline(pos_x, pos_y, influence_radius, arcade.color.PINK)

        draw_time = timeit.default_timer() - draw_start_time

        fps = 1.0 / draw_time

        arcade.draw_text("frame_count: %6d" % self.frame_count, 10, self.height - 14, arcade.color.BLACK, 12)
        arcade.draw_text("delta_time: %12.6f" % self.last_delta_time, 10, self.height - 32, arcade.color.BLACK, 12)
        arcade.draw_text("fps:       %12.6f" % fps, 10, self.height - 50, arcade.color.BLACK, 12)
        arcade.draw_text("scale:     %12.6f" % self.scale, 10, self.height - 68, arcade.color.BLACK, 12)

    def update(self, delta_time):
        self.last_delta_time = delta_time
