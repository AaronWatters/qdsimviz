
from qdsimviz import ballSim
import H5Gizmos as gz

if __name__ == "__main__":
    sim = ballSim.BallSim()
    gz.serve(sim.display())
    