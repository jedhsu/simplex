"""

    *Interpretation*

  A glimpse sample, representing a future fractum.

  Extends fractum with glimpsing information.

"""
from dataclasses import dataclass

from fractal.fractum import Fractum

f64 = float
Heat = int


@dataclass
class Interpretation(
    Fractum,
):
    energy: Heat
    until_end: int
    times: int


"""

Type of a training sample. A sample features the following fields:

- `s::State` is the state
- `π::Vector{Float64}` is the recorded MCTS policy for this position
  * Energy is the discounted reward cumulated from a quantum state.
  * until_end is the (average) number of moves remaining before the end of the game
- `n::Int` is the number of times the state `s` was recorded

As revealed by the last field `n`, several samples that correspond to the
same state can be merged, in which case the `π`, `z` and `t`
fields are averaged together.
"""
