from simulating_blobs_of_fluid.simulation import Simulation


def main():
    simulation = Simulation()

    for _ in range(10):
        simulation.step()


if __name__ == "__main__":
    main()
