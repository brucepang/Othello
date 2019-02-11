Heuristics design:

I implemented the idea from Sannidhanam's paper. Their work An Analysis of Heuristics in Othello thoroughly introduces the Othello game and elaborates a lot on the heuristics. I implement coin parity, mobility, and corner capture mentioned in their paper. Coin parity means the difference between their number of coins. This one is direct and straightforward, similar with the given greedy method. Mobility is to measure the scope of each color's next potential move. The more legal move, the better. Corner is the most important position in othello since it is so stable that it can never be fipped by the opponent. So standing on a position that is can potentially capture will provide a lot value. But directly moving to one of the corner is the best. If in a turn you can move there, do not hesitate.

Algorithm:
Right now I am using depth equal to 2 which means the first layer of the search tree will move to the state that has the maximum score. The second layer of will move to the state that has the minimum score. And that's it.


Experiments:

1. The total number of nodes generated

Every time I execute a move, I treat it as a node generation and I record it. Then through the whole game, I recorded the total number of nodes generated in each move. Then I calculated the average total number of nodes generated for each move. 

The result for minimax is 88.90322580645162.
The result for minimax with alpha-beta pruning is 49.46875.

We can see a significant decrease of number of nodes generated in the alpha-beta case. It makes sense since the pruning essentially skips subtree that is guranteed to be useless.


2. The number of nodes containing states that were generated previously, i.e.
duplicated nodes




3. The average branching factor of the search tree

In each search tree, the branching factor is the number of legal move. I first calculated an average within one search tree and then calculated a overall average on all moves.

The result for minimax is 6.590215359411615
The result for minimax with alpha-beta pruning is 5.402791070936233

This reduction also attributes to the alpha-beta pruning. It essentially eliminates many branches of the search tree and effectively cut the average depth too. As the depth goes, intuitively more moves will be available. So cutting branches can help avoid to go deeper and branch more.


4. The runtime of the algorithm to explore the tree up to a depth of D, for different
values of D

The runtime is determined by the depth of the tree and the average branching factor. 
The naive minimax algorithm has a runtime of O(b^D) where b is the branching factor and can be replaced by the value I observed above.
For minimax with alpha-beta pruning, on average, the runtime is still O(b^D) which based on the assumption that the branching factor is constant. However in most cases, the effective branching factor does decrease, like what I observed above. And the runtime can be expressed as O(5.402^D).
In the best case, all moves are executed in an optimal or near optimal order and the pruning reduces the effective depth to slightly more than half that of naive minimax. It will give O(b^(D/2)).