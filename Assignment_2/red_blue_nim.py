import sys

class State:
    def __init__(self, remainBMarbles, remainRMarbles, version, player, depth, computer, human, alpha, beta):
        self.remainBMarbles = int(remainBMarbles)
        self.remainRMarbles = int(remainRMarbles)
        self.version = version
        self.player = player
        self.depth = int(depth)
        self.computer = computer
        self.human = human
        self.alpha = int(alpha)
        self.beta = int(beta) 

class Player:
    def __init__(self, entity, playerBMarbles, playerRMarbles):
        self.entity = entity
        self.playerBMarbles = int(playerBMarbles)
        self.playerRMarbles = int(playerRMarbles)

class Action:
    def __init__(self, marble_color, marbles_taken):
        self.marble_color = marble_color
        self.marbles_taken = int(marbles_taken)
        self.utility = 0

def player_score(player):
    score = (player.playerBMarbles*3) + (player.playerRMarbles*2) 
    return score

def take_action(state,action,computer,human): # After taking an action, the game state changes. Configure the game state 
    # Take Action Message
    if((action.marble_color == "B") and ((state.player).entity == "computer")):
        if(action.marbles_taken == 1):
            print("Computer takes", action.marbles_taken, "blue marble.\n")
        else:
            print("Computer takes", action.marbles_taken, "blue marbles.\n")
    elif((action.marble_color == "R") and ((state.player).entity == "computer")):
        if(action.marbles_taken == 1):
            print("Computer takes", action.marbles_taken, "red marble.\n")
        else:
            print("Computer takes", action.marbles_taken, "red marbles.\n")
    elif((action.marble_color == "B") and ((state.player).entity == "human")):
        if(action.marbles_taken == 1):
            print("You take", action.marbles_taken, "blue marble.\n")
        else:
            print("You take", action.marbles_taken, "blue marbles.\n")
    elif((action.marble_color == "R") and ((state.player).entity == "human")):
        if(action.marbles_taken == 1):
            print("You take", action.marbles_taken, "red marble.\n")
        else:
            print("You take", action.marbles_taken, "red marbles.\n")

    # Things that will change: remaining marbles, player marbles, and the current player, alpha and beta values set to -infinity and +infinity for computer's turn
    if((action.marble_color == "B")): # Marble picked is blue
        state.remainBMarbles = state.remainBMarbles - action.marbles_taken
    else: # Marble picked is red
        state.remainRMarbles = state.remainRMarbles - action.marbles_taken
    if((state.player).entity == "computer"): # current player is computer, next turn is human.
        state.player = human
    else: # current player is human, next turn is computer.
        state.player = computer

    state.alpha = -(sys.maxsize)
    state.beta = sys.maxsize

    return state

def print_marble_stacks(state):
    print("-------------------------------")   
    print("Remaining Blue Marbles: " , state.remainBMarbles)
    print("Remaining Red Marbles: " , state.remainRMarbles)
    print("-------------------------------\n")   

def is_integer(s):
    return s.isdigit()

def config_init_state(arguments,state,computer,human):
    if(len(arguments)!=2): # User gave more than bare minimum arguments, must reconfigure default state values for <version> and <first-player> .
        if(len(arguments)==3): # User gave one optional argument, don't consider default attributes case.
            if((arguments[2]=="human")or(arguments[2]=="Human")):
                state.player = human
            elif(arguments[2]=="misere")or(arguments[2]=="Misere"):
                state.version = "misere"
            elif(is_integer(arguments[2])):
                state.depth = arguments[2]
        elif(len(arguments)==4): # User gave atleast 2 optional arguments, don't configure default attributes case.
            if((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="human")or(arguments[3]=="Human")):
                state.version = "misere"
                state.player = human
            elif((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="computer")or(arguments[3]=="Computer")):  
                state.version = "misere"
            elif((arguments[2]=="standard")or(arguments[2]=="Standard") and (arguments[3]=="human")or(arguments[3]=="Human")):  
                state.player = human
            elif((arguments[2]=="misere")or(arguments[2]=="Misere") and is_integer(arguments[3])):
                state.version = "misere"
                state.depth = arguments[3]
            elif((arguments[2]=="human")or(arguments[2]=="Human") and is_integer(arguments[3])):
                state.player = human
                state.depth = arguments[3]
        elif(len(arguments)==5): # User gave all arguments.
            state.depth = int(arguments[4])
            if((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="human")or(arguments[3]=="Human")):
                state.version = "misere"
                state.player = human
            elif((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="computer")or(arguments[3]=="Computer")):  
                state.version = "misere"
            elif((arguments[2]=="standard")or(arguments[2]=="Standard") and (arguments[3]=="human")or(arguments[3]=="Human")):  
                state.player = human

def query_marble_color():
    marble_color = input("Choose Marble (B/R): ").rstrip()
    if(marble_color == "b"):
        marble_color = "B"
    elif(marble_color == "r"):
        marble_color = "R"
    while((marble_color != "B") and (marble_color != "R")):
        marble_color = input("Choose Marble (B/R): ").rstrip()
        if(marble_color == "b"):
            marble_color = "B"
        elif(marble_color == "r"):
            marble_color = "R"
    return marble_color

def query_marbles_taken(state, marble_color):
    marbles_taken = input("Choose Amount (1/2): ").rstrip()
    if(marble_color == "B"):
        while((marbles_taken != "1") and (marbles_taken != "2") or (state.remainBMarbles < int(marbles_taken))):
            marbles_taken = input("Choose Amount (1/2): ").rstrip()
    else:
        while((marbles_taken != "1") and (marbles_taken != "2") or (state.remainRMarbles < int(marbles_taken))):
            marbles_taken = input("Choose Amount (1/2): ").rstrip()
    
    return marbles_taken

def end_of_game(state):
    if(((state.player).entity == "computer") and (state.version == "standard")):
        print("You Won")
    elif(((state.player).entity == "human") and (state.version == "standard")):
        print("Game Over")
    elif(((state.player).entity == "computer") and (state.version == "misere")):
        print("Game Over")
    elif(((state.player).entity == "human") and (state.version == "misere")):
        print("You Won")

def successor_state(action, state): # works similarily like take_action(), used in the alpha-beta decision algorithm for the computer's decision. Returns the successor state after taking an action
    computer = Player("computer", (state.computer).playerBMarbles, (state.computer).playerRMarbles)
    human = Player("human", (state.human).playerBMarbles, (state.human).playerRMarbles)

    if((state.player).entity == "human"): # current player is human, successor state is computer's turn.
        successor = State(state.remainBMarbles, state.remainRMarbles, state.version, computer, state.depth+1, computer, human, state.alpha, state.beta)
    else: # current player is human, successor state is computer's turn.
        successor = State(state.remainBMarbles, state.remainRMarbles, state.version, human, state.depth+1, computer, human, state.alpha, state.beta)

    if((action.marble_color == "B")): # Marble picked is blue
        successor.remainBMarbles = successor.remainBMarbles - action.marbles_taken
    else: # Marble picked is red
        successor.remainRMarbles = successor.remainRMarbles - action.marbles_taken

    return successor

def possible_actions(state)
    # 

def successors(state)
    actionsList = possible_actions(state) # returns a list of possible actions for a given state
    successorStateList = []
    for action in actionsList: 
        successorStateList.apend(successor_state(action,state))
    return successorStateList

def utility(state):

def terminal_test(test):

def max_util(actions): # returns the higest utility among a list of actions

# def min_util(actions):

def find(util, actions) # Maps the given utility to the first corresponding action in the action list. Returns found action

def max_value(state):
    util = utility(state)
    if (terminal_test(state) == True)
        return util
    v = -(sys.maxsize)

    successorStateList = successors(state)

    for s in successorStateList:
        v = max(v, min_value(s))
        if(v>=state.beta)
            return v
        state.alpha = max(state.alpha,v)
    
    return v

def min_value(state):
    util = utility(state)
    if (terminal_test(state) == True)
        return util
    v = sys.maxsize

    successorStateList = successors(state)

    for s in successorStateList:
        v = min(v, max_value(s))
        if(v<=state.alpha)
            return v
        state.beta = min(state.beta,v)
    
    return v

def alpha_beta_decision(state):
    # Configure the alpha and beta values
    state.alpha = -(sys.maxsize)
    state.beta = sys.maxsize

    actionsList = possible_actions(state) # returns a list of possible actions for a given state
    for action in actionsList: 
        action.utility = min_value(successor_state(action, state)) # for each possible action we configure it's payoff (utility)
    utility = max_util(actionsList) # returns the higest utility among the actions in actionList
    return find(util, actionsList) # returning the action with the highest utility





def main():
    if(len(sys.argv)<3):
        print("Not enough arguments\n")
        sys.exit()

    arguments = sys.argv[1:] # Arguments passed: <num red> <num blue> <version> <first-player> <depth>.
    computer = Player("computer", 0, 0)
    human = Player("human", 0, 0)
    state = State(arguments[0], arguments[1], "standard", computer, 0, computer, human, -(sys.maxsize), sys.maxsize) # Default state attributes set.

    config_init_state(arguments,state,computer,human) # Reconfigure state attributes based on the passed arguments

    print("\n_______________________________Nim Game_______________________________")
    while((state.remainBMarbles>0) and (state.remainRMarbles>0)):
        if((state.player).entity == "computer"):
            print("\n=====Computer=====")

            action = alpha_beta_decision(state)
            state = take_action(state, action, computer, human)

            state.player = human

        else: #player turn
            print("\n=====Player=====")
            print_marble_stacks(state)

            marble_color = query_marble_color()
            marbles_taken = query_marbles_taken(state, marble_color)

            action = Action(marble_color, marbles_taken)

            state = take_action(state,action,computer,human)
    end_of_game(state)


if __name__ == "__main__":
    main()

# - Arguments:
# 	- num red (req)
# 	- num blue (req)
# 	- version (standard or misere)
# 	- first-player (human or computer, computer is the default option)
# 	- depth (for extra credit)
# - Switch b/w player and opponent turns
# 	- on turn, pick a pile
# 	- on turn, remove one marble
# 	- on turn, remove two marbles
# - two stacks of marbles, red and blue marbles
# 	- amount given in arguments
# 	- red marbles worth 2
# 	- blue marbles worth 3
# - standard and misere ver
# 	- loss condition in standard: either pile is empty on player's turn.
# 	- win condition in misere ver: either pile is empty on player's turn.
# 	- remaining marbles determine winning points
# - computer opponent is the optimal player
# 	- MinMax w/ Alpha Beta Prunning 