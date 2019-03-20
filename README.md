# 17th-automaton
A Python made program for solving the statement of Topic 17.

## Requisites
Python 3.4 and above (tested on Python 3.6.8). It can be downloaded [here](https://www.python.org/downloads/).

## Where to download
It can be downloaded [right here](https://github.com/MaanuelMM/17th-automaton/releases/latest) (choose between ZIP or TAR.GZ as you prefer).

## Initial setup
Extract it and open a terminal window on the directory where it was extracted.

## How to use
Execute `main.py` in terminal and follow the instructions to add and convert automata.
```
python main.py
```

## Demostration
Execute `demo.py` in terminal to convert the automata example.
```
python demo.py
```

## How it works
### Statement
Given a finite automaton (*A*), it is asked to write a finite automaton (*A’*) that fulfills the following condition:
* *L(A’)={xy, x ∈ L(A), y ∉ L(A)}*
### Steps for solving the problem
1. Convert the finite automaton to a complete deterministic one.
   - *Algorithm to eliminate empty transitions (lambda).*
   - *Algorithm for converting a NFA to a DFA.*
   - *Reduce DFA: no useless states (not accessible and not co-accessible).*
   - *Complete DFA: for each pair (state, letter) there is transition -> "dead state".*
2. Calculate complement of the complete DFA from the previous step.
   - *As the DFA is complete, it will be enough to indicate that the final states are not and vice versa.*
3. Concatenate the DFA calculated in the first step with its complement calculated in the second step.
   - *It will be enough to create empty transitions (lambda) between the set of final states of the first automaton and the initial state of the second automaton, being the new set of final states those of the second automaton.*
4. OPTIONAL: eliminate the empty transitions (lambda) of the previous step.
   - *This step is performed by the program; however, in the example below it has not been performed to facilitate the understanding of the algorithm.*

## Example
### Input data
* **First automaton**
![First automaton](/example/img/first_automaton.png)

* **Second automaton**
![Second automaton](/example/img/second_automaton.png)

### Output data
**NOTE**: the automata presented in this README have lambda transitions to make them easier to understand. This program returns automata without lambda transitions.
* **First automaton**
![First automaton converted](/example/img/first_automaton_converted.png)

* **Second automaton**
![Second automaton converted](/example/img/second_automaton_converted.png)
