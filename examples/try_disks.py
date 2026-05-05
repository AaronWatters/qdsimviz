
from qdsimviz import disksSim
import H5Gizmos as gz

if __name__ == "__main__":
    sim = disksSim.DisksSim()
    gz.serve(sim.display())