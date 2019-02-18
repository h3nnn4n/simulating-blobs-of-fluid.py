import multiprocessing

from functools import partial
from math import sqrt
from random import uniform

from .particle import Particle
from .vector import Vector


def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    if func_name.startswith('__') and not func_name.endswith('__'):  # deal with mangled names
        cls_name = cls.__name__.lstrip('_')
        func_name = '_' + cls_name + func_name
    return _unpickle_method, (func_name, obj, cls)


def _unpickle_method(func_name, obj, cls):
    for cls in cls.__mro__:
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

import copyreg
import types
copyreg.pickle(types.MethodType, _pickle_method, _unpickle_method)


class SimulationParallel:
    def __init__(self, particle_count=100, dt=0.25, box_width=1000):
        self.particle_count = particle_count
        self.dt = dt
        self.gravity = Vector(0, -9.8).normalize()

        self.stiffness = 35 * 0.025
        self.stiffness_near = 100 * 0.025
        self.rest_density = 10

        self.box_width = box_width
        self.box_height = self.box_width
        self.box_radius = self.box_width
        self.box_radius_squared = self.box_radius**2
        self.grid_size = 50
        self.iteraction_radius_size = 10
        self.iteraction_radius_size_squared = self.iteraction_radius_size**2
        self.iteraction_radius = int((self.iteraction_radius_size / self.box_width) * self.grid_size)

        self.particles = [Particle() for _ in range(self.particle_count)]
        self.scatter_particles()

        self.grid_hash = {}

        self.pool = multiprocessing.Pool(8)

    def scatter_particles(self):
        for particle in self.particles:
            particle.position.random().set_mag(uniform(0, self.box_radius))
            particle.old_postion.set(particle.position).random_move()
            particle.velocity.random()

    def step(self):
        self.grid_hash.clear()
        self.pool.map(self.pass_1, enumerate(self.particles))
        self.pool.map(self.pass_2, enumerate(self.particles))
        self.pool.map(self.pass_3, enumerate(self.particles))

    def pass_1(self, index, particle):
        particle.update_old_postition()

        particle.apply_force(self.gravity, self.dt)

        particle.update_position(self.dt)
        self.hash_store(particle.position, index)

    def pass_2(self, index, _):
        neighbours = self.get_neighbours_with_gradient(index)
        self.update_densities(index, neighbours)
        self.relax(index, neighbours, self.dt)

    def pass_3(self, _, particle):
        self.contain(particle)
        self.update_velocity(particle)

    def get_neighbours_with_gradient(self, index):
        neighbours = []
        particle = self.particles[index]
        grid_pos = self.gridify(particle.position)
        results = self.hash_get(grid_pos, radius=self.iteraction_radius)

        for result in results:
            if result == index:
                continue

            gradient = self.gradient(index, result)

            if gradient == 0:
                continue

            particle.gradient = gradient

            neighbours.append(result)

        return neighbours

    def update_densities(self, index, neighbours):
        density = 0
        density_near = 0

        for neighbor in neighbours:
            gradient = self.particles[neighbor].gradient

            gradient_squared = gradient * gradient
            density += gradient_squared
            density_near += gradient_squared * gradient

        particle = self.particles[index]

        particle.pressure = self.stiffness * (density - self.rest_density)
        particle.pressure_near = self.stiffness_near * density_near

    def relax(self, index, neighbours, dt):
        particle = self.particles[index]

        force = Vector(1, 1)

        for neighbor in neighbours:
            neighbor_particle = self.particles[neighbor]
            neighbor_position = neighbor_particle.position
            gradient = neighbor_particle.gradient

            magnitude = particle.pressure * gradient + particle.pressure_near * gradient * gradient
            force.set(particle.position - neighbor_position)
            force.set_mag(magnitude)

            particle.position.x += force.x * -0.5
            particle.position.y += force.y * -0.5

            neighbor_position.x += force.x * 0.5
            neighbor_position.y += force.y * 0.5

    def gradient(self, index, neighbor_index):
        particle1 = self.particles[index]
        particle2 = self.particles[neighbor_index]

        distance_squared = particle1.position.distance_squared(particle2.position)

        if distance_squared > self.iteraction_radius_size_squared:
            return 0

        distance = sqrt(distance_squared)

        return 1.0 - (distance / self.iteraction_radius_size)

    def contain(self, particle):
        if particle.position.norm_squared <= self.box_radius_squared:
            return

        particle.position.set_mag(self.box_radius)
        particle.old_postion.set_mag(self.box_radius + 2.5)

    def update_velocity(self, particle):
        velocity = (particle.position - particle.old_postion) * (1 / self.dt)
        particle.velocity.set(velocity)

    def hash_store(self, vector, index):
        grid_pos = self.gridify(vector)

        if grid_pos not in self.grid_hash.keys():
            self.grid_hash[grid_pos] = []

        self.grid_hash[grid_pos].append(index)

    def hash_get(self, key, radius=1):
        values = []

        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if sqrt(i**2 + j**2) > radius:
                    continue

                grid_pos = key[0] + i, key[1] + j
                if grid_pos not in self.grid_hash.keys():
                    continue

                values.extend(self.grid_hash[grid_pos])

        return values

    def gridify(self, vector):
        grid_x = int((vector.x / self.box_width + 0.5) * self.grid_size)
        grid_y = int((vector.y / self.box_height + 0.5) * self.grid_size)

        return (grid_x, grid_y)