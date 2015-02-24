========================================
crossword puzzle generator by python
========================================

Generate crossword puzzles with given words in a heuristic way.

python run.py <word list file>

$ python run.py words.short
#LOVEE#
score: 8.000000

_#_____
_I_____
#LOVEE#
_K_____
_#_____
score: 3.000000

_____#_#_
#BEROB#T_
_####ACE#
#INERT#M_
#LOVEE#P_
#KNEED#T_
_#####_#_
score: 0.132231

...

run.py tries to show valid and more useful results as early as possible.

Algorithm
-----------------

Staring from a randomly choosen word, every possible combinations
of words which can be placed with already embedded words are tried.
When there is no possible words (in the given list) which might be
able to be placed onto more than two connected characters, the pattern
is discarded.

All combinations are stacked on memory.
It will crash when used up all available memory.

Currently it executes on a single thread.
It should be easy to make it multi-threaded.


Structure
-----------------
crossword.py contains basic functionality (OpenGrid, Grid) and
obsolete approach (Crossword).

crossword2.py contains new approach.

run.py just invokes crossword2.py.

test*.py are for random experiments.
