# Schelling's Model of Segregation: the description of a quick implementation

## Introduction
The social segregation has always been a problem among the United States. However, this problem is harder to resolve than it appears to be.

In 1971, the American economist Thomas Schelling created a model that describes what happens to the population if people tend to move next to their similar — considering that even for this minimalistic population in the model, which does not suffer from racism and any prejudice, people will still segregate.

The purpose of this article is to describe how this model works by guiding the reader through a fast Python implementation.

## The Segregation Model
The model describes the population positioned geographically in an NxN matrix, where every cell can assume three values: X, Y, and 0. The X cell represents the X group, the Y cell, the Y group, and the 0 cell indicates that Xs or Ys do not occupy this space, in other words, an empty cell. _Figure 1_ represents the actors of the system.

![Figure 1 - the Actors](https://github.com/victorgcramos/decentralized-governance-tcc/blob/implementation-description/simulations/schelling-model/images/tcc-governance-diagrams-schelling.png?raw=true)
> Figure 1 - the Actors.

Primarily, the cells are disposed of randomly given the proportion of empty and fulfilled spaces. _Figure 2_ represents a model for a 50x50 **geographical matrix** where 20% of the cells are void spaces.

![Figure 2 - Initial State for a 50x50 matrix with 20% of empty spaces](https://github.com/victorgcramos/decentralized-governance-tcc/blob/implementation-description/simulations/schelling-model/images/50x50-100x-08-before.png?raw=true)
> Figure 2 - Initial State for a 50x50 matrix with 20% of empty spaces.

### The Iterative Method - Rounds
The Schelling model is iterative over every cell of the matrix. Every **round** is composed of the comparison step and the moving stage.

#### The Comparison Step
Every cell (A) has a neighborhood formed by its eight closest cells, as illustrated in _Figure 3_. The proportion between cells of type A and occupied cells indicates the `similarity` level.

![Figure 3 - The Neighborhood](https://github.com/victorgcramos/decentralized-governance-tcc/blob/implementation-description/simulations/schelling-model/images/schelling-iteration-1-neighborhood-1.png?raw=true)

> Figure 3 - The Neighborhood. 


There are two referenced cells on _Figure 3_: **A** and **B**. Both **A** and its neighborhood have a red outline, and the `similarity` is 66%. On the other hand, **B** (blue) is surrounded with only one similar to him, so the similarity is 28%

#### The Moving Step
 If the `similarity` level is higher or equal the `threshold`, the cell stays in the same place. Otherwise, the cell moves to the closest empty cell. In this case, the **A** `similarity` is 66%, which is higher than the `threshold`, so **A** stays in the same place. Contrary, **B** has a `similarity` index below the threshold, so **B** is moving to the next empty _(purple)_ cell.

 > Threshold - number that establishes the limit of similarity. The current example indicates a threshold of 50%.

 ### The Iterative Method - Rounds Iterating over the NxN Matrix
 Each iteration is represented by the aggregate of NxN rounds. Once every cell realizes the procedure described by the **round**, one iteration is completed. As a consequence of similarity seeking, the **geographical matrix** described by _Figure 4_ represents the segregation process happening for this population **after 100 iterations**. _Figure 5_ represents the process **after 400 iterations**.

 ![Figure 4 - The segregation process after 100 iterations](https://github.com/victorgcramos/decentralized-governance-tcc/blob/implementation-description/simulations/schelling-model/images/50x50-100x-08-after.png?raw=true)
 > Figure 4 - The segregation process after 100 iterations

 ![Figure 5 - The segregation process after 400 iterations](https://github.com/victorgcramos/decentralized-governance-tcc/blob/implementation-description/simulations/schelling-model/images/50x50-400x-08-after-1.png?raw=true)
 > Figure 5 - The segregation process after 400 iterations

## Conclusion
After iterating the model over multiple times, the conclusion taken from the procedure described is that the segregation happens regardless of racism and other social prejudices. Even for a system that is apart of these human variables, the decregation still occurs.

With the approach described by Thomas Schelling, the ability of using computational simulations can be used to support some cientifical hypotheses, by improving the method that the results are taken.

## References
1. McCown, Frank. “Schelling’s Model of Segregation.” Stanford.Edu, nifty.stanford.edu/2014/mccown-schelling-model-segregation/. Accessed 5 July 2019.
2. Schelling, Thomas C. “Dynamic Models of Segregation†.” The Journal of Mathematical Sociology, vol. 1, no. 2, July 1971, pp. 143–186, 10.1080/0022250x.1971.9989794. Accessed 5 July 2019.