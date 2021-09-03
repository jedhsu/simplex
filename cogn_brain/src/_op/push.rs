//! Compute the forward pass of a network on a batch of inputs.
//! 
//! Expect a `Float32` tensor `states` whose batch dimension is the last one.

pub struct Push(Brain):
    // TODO clarify
    fn push(&self) -> (Parameters, States);


    // forward(::AbstractNetwork, states)



// Return a `(P, V)` triple where:

//   - `P` is a matrix of size `(num_actions, batch_size)`. It is allowed
//     to put weight on invalid actions (see <`evaluate`>(@ref)).
//   - `V` is a row vector of size `(1, batch_size)`
// \\\!