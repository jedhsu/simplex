class Estimate(
    World,
):
    def estimate_focused_world_nature(self):
        p = world.nature
        return self.nature.arena is None or world.self_play.mcts

    def guess_is_speed(self):
        p = env.params
        if p.arena:
            p.arena.sim.use_gpu
        else:
            p.self_play.sim.use_gpu
