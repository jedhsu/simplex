"""

    *Stones*

  Hyperparmaeters.

"""

from dataclasses import dataclass

@dataclass
class Parameters:
    self_play: SelfPlayParams
    learning: LearningParameters
    arena: ArenaParameters
    num_iters: Int
    memory_analysis: MemoryAnalysisParameters = None
    use_symmetries: Bool = false
    ternary_rewards: Bool = false
    mem_buffer_size: PLSchedule{Int}

"""

The AlphaZero training process consists in `num_iters` iterations. Each
iteration can be decomposed into a self-play phase
(see [`SelfPlayParams`](@ref)) and a learning phase
(see [`LearningParams`](@ref)).

  - `ternary_rewards`: set to `true` if the rewards issued by
     the game environment always belong to ``\\{-1, 0, 1\\}`` so that
     the logging and profiling tools can take advantage of this property.
  - `use_symmetries`: if set to `true`, board symmetries are used for
     data augmentation before learning.
  - `mem_buffer_size`: size schedule of the memory buffer, in terms of number
     of samples. It is typical to start with a small memory buffer that is grown
     progressively so as to wash out the initial low-quality self-play data
     more quickly.
  - `memory_analysis`: parameters for the memory analysis step that is
     performed at each iteration (see [`MemAnalysisParams`](@ref)), or
     `nothing` if no analysis is to be performed.

# AlphaGo Zero Parameters

In the original AlphaGo Zero paper:
- About 5 millions games of self-play are played across 200 iterations.
- The memory buffer contains 500K games, which makes about 100M samples
  as an average game of Go lasts about 200 turns.
"""

# for T in [MctsParams, SimParams, ArenaParams, SelfPlayParams, LearningParams, Params]
#   Util.generate_update_constructor(T) |> eval
# end
