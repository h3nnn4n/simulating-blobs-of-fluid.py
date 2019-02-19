from simulating_blobs_of_fluid.simulation import Simulation

import timeit


def main():
    simulation = Simulation(particle_count=2000)

    n_iters = 20
    total_fps = 0
    total_time = 0

    for iter in range(n_iters):
        start = timeit.default_timer()
        simulation.step()
        end = timeit.default_timer()
        time = end - start
        print("%3d %10.6f %10.6f" % (iter, time, 1 / time))

        total_fps += 1 / time
        total_time += time

    print("%10.6f %10.6f" % (total_time / n_iters, total_fps / n_iters))


if __name__ == "__main__":
    main()
