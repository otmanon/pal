import polyscope as ps
import numpy as np

from .World import WorldParams

from sims import PinnedPendulum, PinnedPendulumState
from sims.PinnedPendulum import PinnedPendulumParams

class PinnedPendulumWorldRenderer():
    def __init__(self, init_state : PinnedPendulumState = PinnedPendulumState(), y=np.array([[0], [-1]])):
        ps.init()
        self.X = np.concatenate((np.array([[0, 0]]), init_state.x.reshape(-1, 2)), axis=0)

        self.Y = np.concatenate((np.array([[0, 0]]), y.reshape(-1, 2)), axis=0)
        ps.register_curve_network("pendulum", self.X, np.array([[0, 1]]), enabled=True, radius=0.03, color=[0, 0, 1])
        ps.register_point_cloud("points", self.X, radius=0.1, color=[0, 0, 1])
        ps.register_curve_network("pendulum_target", self.Y, np.array([[0, 1]]), enabled=True, radius=0.03, color=[1, 0, 0])
        ps.register_point_cloud("points_target", self.Y, radius=0.1, color=[1, 0, 0])
        ps.set_ground_plane_mode("none")
        ps.look_at([0, -0.5, 3], [0, -0.5, 0])
        return

    def render(self, state : PinnedPendulumState):
        self.X[1, :] = state.x.reshape(-1, 2)
        ps.get_curve_network("pendulum").update_node_positions(self.X)
        ps.get_point_cloud("points").update_point_positions(self.X)
        ps.frame_tick()
        return



class PinnedPendulumWorldParams(WorldParams):
    def __init__(self, render=False, init_state : PinnedPendulumState = PinnedPendulumState(), sim_params : PinnedPendulumParams =PinnedPendulumParams()):
        self.render = render
        self.sim_params = sim_params
        self.init_state = init_state
        return


class PinnedPendulumWorld():
    def __init__(self, p : PinnedPendulumWorldParams = PinnedPendulumWorldParams()):
        self.p = p
        self.sim = PinnedPendulum(self.p.sim_params)


        if self.p.render:
            self.renderer = PinnedPendulumWorldRenderer(self.p.init_state, self.p.sim_params.y)
        self.reset()
    def step(self):
        self.sim_state = self.sim.step_sim(self.sim_state)



        if self.p.render:
            self.renderer.render(self.sim_state)

        return

    def reset(self):
        self.sim_state = PinnedPendulumState(self.p.init_state.x)

        if self.p.render:
            self.renderer.render(self.sim_state)

        pass


