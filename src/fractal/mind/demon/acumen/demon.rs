//! A generic, standalone implementation of Monte Carlo Tree Search.
//! It can be used on any game that implements `GameInterface`
//! and with any external oracle.


An oracle can be any function or callable object.
  
   oracle(state)

evaluates a single state from the current player's perspective and returns 
a pair `(P, V)` where:

  - `P` is a probability vector on `GI.available_actions(GI.init(gspec, state))`
  - `V` is a scalar estimating the value or win probability for white.
\\\!

module MCTS

using Distributions: Categorical, Dirichlet

using ..AlphaZero: GI, Util

#####
##### Standard Oracles
#####


//! Acumen empowers the mind to estimate the value of a position by simulating a random game
//! from it (a rollout). Moreover, it puts a uniform prior on available actions.
//! Therefore, it can be used to implement the "vanilla" MCTS algorithm.

pub struct Acumen {
    nature: Nature,
    decay :: Float64,
    // RolloutOracle(gspec, γ=1.) = new{typeof(gspec)}(gspec, γ)
}

function rollout!(game, γ=1.)
  r = 0.
  while !GI.game_terminated(game)
    action = rand(GI.available_actions(game))
    GI.play!(game, action)
    r = γ * r + GI.white_reward(game)
  end
  return r
end
function (r::RolloutOracle)(state)
  g = GI.init(r.gspec, state)
  wp = GI.white_playing(g)
  n = length(GI.available_actions(g))
  P = ones(n) ./ n
  wr = rollout!(g, r.gamma)
  V = wp ? wr : -wr
  return P, V
end

# AlphaGo Zero Parameters

In the original AlphaGo Zero paper:

+ The discount factor `gamma` is set to 1.
+ The number of MCTS iterations per move is 1600, which
  corresponds to 0.4s of computation time.
+ The temperature is set to 1 for the 30 first moves and then to an
  infinitesimal value.
+ The ``ϵ`` parameter for the Dirichlet noise is set to ``0.25`` and
  the ``α`` parameter to ``0.03``, which is consistent with the heuristic
  of using ``α = 10/n`` with ``n`` the maximum number of possibles moves,
  which is ``19 × 19 + 1 = 362`` in the case of Go.
\\\!
@kwfn struct MctsParams
  gamma :: Float64 = 1.
  cpuct :: Float64 = 1.
  num_iters_per_turn :: Int
  temperature :: AbstractSchedule{Float64} = ConstSchedule(1.)
  dirichlet_noise_ϵ :: Float64
  dirichlet_noise_α :: Float64
  prior_temperature :: Float64 = 1.
end

\\\!
    SamplesWeighingPolicy

During &self-play, early board positions are possibly encountered many
times across several games. The corresponding samples can be merged
together and given a weight ``W`` that is a nondecreasing function of the
number ``n`` of merged samples:

  - `CONSTANT_WEIGHT`: ``W(n) = 1``
  - `LOG_WEIGHT`: ``W(n) = \\log_2(n) + 1``
  - `LINEAR_WEIGHT`: ``W(n) = n``
\\\!
@enum SamplesWeighingPolicy CONSTANT_WEIGHT LOG_WEIGHT LINEAR_WEIGHT
