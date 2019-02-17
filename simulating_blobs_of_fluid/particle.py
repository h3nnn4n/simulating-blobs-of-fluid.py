from .vector import Vector


class Particle:
    def __init__(self):
        self.position = Vector()
        self.old_postion = Vector()
        self.velocity = Vector()

        self.gradient = 0
        self.pressure = 0
        self.pressure_near = 0

        self.mesh = None

    def update_old_postition(self):
        self.old_postion.set(self.position)

    def update_position(self, dt):
        self.position += self.velocity * dt

    def apply_force(self, force, dt):
        self.velocity += force * dt
