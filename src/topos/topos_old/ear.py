"""

    launch_server(f; num_workers, batch_size)

Launch an inference requests server.
function launch_server(f; num_workers, batch_size)
  @assert batch_size <= num_workers
  channel = Channel(num_workers)
  # The server is spawned on the main thread for maximal responsiveness
  Util.@tspawn_main Util.@printing_errors begin
    num_active = num_workers
    pending = []
    while num_active > 0
      req = take!(channel)
      if req == :done
        num_active -= 1
        if num_active < batch_size
          batch_size = num_active
        end
      else
        push!(pending, req)
      end
      @assert length(pending) <= num_active
      @assert batch_size <= num_active
      if length(pending) >= batch_size && length(pending) > 0
        batch = [p.query for p in pending]
        results = f(batch)
        for i in eachindex(pending)
          put!(pending[i].answer_channel, results[i])
        end
        empty!(pending)
      end
    end
  end
  return channel
end

"""
# Arguments

  - `f` is the function to be evaluated (e.g. a neural network).
    It takes a batch of inputs and returns a batch of results
    of similar size.
  - `num_workers` is the number of workers that are expected to
    query the server.
  - `batch_size` corresponds to the batch size that is used to evaluate `f`.
    Note that one must have `batch_size <= num_workers`

# How to use

This function returns a channel along which workers can send queries.
A query can be either:

    - `:none` when a worker is done and about to terminate
    - a named tuple with fields `query` (the input to be given to `f`) and
      `answer_channel` (the channel the sever must use to return its answer).

The server stops automatically after all workers send `:none`.
"""

"""
    finished(reqc)

This function is to be called every time a client to the inference server identified
by request channel `reqc` is done and won't send queries anymore.

It should be called ``n`` times in total, where ``n`` is the number of workers that was
indicated to [`launch_server`](@ref).

!!! note

    This function does not take a `BatchedOracle` as an argument as there can be several
    oracles per worker (e.g. a worker can simulate games between two players that each
    rely on a neural network).
"""
finished(reqc) = put!(reqc, :done)

"""
    BatchedOracle(reqc, preprocess=(x->x))

Create an oracle that delegates its job to an inference server.

- When called on a state, this oracle sends a query to the server identified by
  request channel `reqc`. This call is blocking until every other active worker also
  sends its query.
- A `preprocess` function can be provided to ransform the passed state before it is
  sent to the server as a query.
"""

class BatchedDemon{F}
    preprocess :: F
    reqchan :: Channel
    anschan :: Channel
    function BatchedOracle(reqchan, preprocess=(x->x))
        return new{typeof(preprocess)}(preprocess, reqchan, Channel(1))

def (oracle::BatchedOracle)(state)
query = oracle.preprocess(state)
  put!(oracle.reqchan, (query=query, answer_channel=oracle.anschan))
  answer = take!(oracle.anschan)
  return answer
end

