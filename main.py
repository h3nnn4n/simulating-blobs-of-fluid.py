from simulating_blobs_of_fluid.simulation import Simulation
from simulating_blobs_of_fluid.fluid_renderer import FluidRenderer

import arcade


def main():
    simulation = Simulation()
    fluid_renderer = FluidRenderer(200, 800, simulation)

    arcade.run()


if __name__ == "__main__":
    main()
