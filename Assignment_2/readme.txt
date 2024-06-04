Name and ID: Isaac Medrano 1001884307

Programming Language: Python 3.10.12

Code Structure:
The source code is separated into 4 sections:
1. At the top we have the class definitions for a game state and a game action.
2. Afterwards, we have functions that aid the Nim game loop. These functions do not help implement the alpha-beta pruning algorithm.
3. Next is the functions that implement the alpha-beta pruning algorithm. They follow similar structure to the pseudo code provided in class.
    - [Line: 139] successors_state(state): Used in successors. Used together with possible_actions(state) to implement this line in the AlphaBetaDecision(state) pseudo code "return the a in Action(state) leading to a successor state with utility v."
    - [Line: 146] possible _actions(sate): Implements the Actions(state) function in the pseudo code. Function used by successors(state) and alpha_beta_decision(state).
    - [Line: 193] successors(state): Implements the Successors(state) function in the pseudo code
    - [Line: 200] utility(state,player): Implements the Utility(state) function in the pseudo code
    - [Line: 232] terminal_test(state): Implements the TerminalTest(state) function in the pseudo code
    - [Line: 241] max_value(state,alpha,beta): Implements the MaxValue(state,alpha,beta) function in the pseudo code
    - [Line: 256] min_value(state,alpha,beta): Implements the MinValue(state,alpha,beta) function in the pseudo code
    - [Line: 271] depth_limited_max_value(state,alpha,beta,depth): Implements Depth Limited Alpha-Beta Prunning 
    - [Line: 286] depth_limited_min_value(state,alpha,beta,depth): Implements Depth Limited Alpha-Beta Prunning 
    - [Line: 301] alpha_beta_decision(state): Implements AlphaBetaDecision(state) function in the pseudo code. Modified to support regular alpha beta pruning and depth limited alpha beta prunning.
4. A "main()" function that launches and maintains the Nim game loop util the end game.

How to run: 
Run the following command in your terminal: 
python3 red_blue_nim.py <number of red marbles> <number of blue marbles> <version> <first-player> <depth>
Replace python3 with whatever command your machine uses to run Python 3.10.12
<number of red marbles> <number of blue marbles> are the only required command line arguments. A default game is set to run the standard version, no depth limit, with the computer as the first player.
