"benchmark diskSim update using profiling"

from qdsimviz import disksSim

def benchmark_update(iterations=1000):
    sim = disksSim.DisksSim()
    for i in range(iterations):
        if i % 100 == 0:
            print(f"Iteration {i}")
        sim.update(0.016)

if __name__ == "__main__":
    # profile the benchmark using cProfile
    import cProfile
    cProfile.run('benchmark_update()')
