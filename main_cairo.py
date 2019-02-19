from simulating_blobs_of_fluid.simulation import Simulation
from simulating_blobs_of_fluid.context_manager import ContextManager

import timeit
from math import pi


def main():
    simulation = Simulation(particle_count=500, box_width=2000, dt=0.05)
    context_manager = ContextManager()

    n_iters = 20
    total_fps = 0
    total_time = 0
    total_drawing_time = 0
    image_count = 0

    ctx = context_manager.ctx

    scale = context_manager.width / (simulation.box_width * 2)

    for i in range(10001):
        start = timeit.default_timer()
        simulation.step()
        end = timeit.default_timer()
        time = end - start

        total_fps += 1 / time
        total_time += time

        if i % 100 != 0:
            continue

        image_count += 1

        start_drawing = timeit.default_timer()
        context_manager.set_background()
        ctx.set_source_rgb(255, 0, 0)

        for particle in simulation.particles:
            position = particle.position

            pos_x = (position.x + simulation.box_width) * scale
            pos_y = (position.y - simulation.box_height) * -scale

            ctx.arc(pos_x, pos_y, 2, 0, 2 * pi)

            ctx.fill()

        context_manager.save("%06d.png" % image_count)

        end_drawing = timeit.default_timer()
        time_drawing = end_drawing - start_drawing
        total_drawing_time += time_drawing
        print("%6d %10.6f %10.6f %10.6f %10.6f" % (i, time, 1 / time, time_drawing, 1 / time_drawing))

    print(
        "%10.6f %10.6f %10.6f %10.6f" %
        (total_time / n_iters,
         total_fps / n_iters,
         total_drawing_time / image_count,
         1 / (total_drawing_time / image_count)))


if __name__ == "__main__":
    main()
