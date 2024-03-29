import sys

class State:
    def __init__(self, remainRMarbles, remainBMarbles):
        self.remainRMarbles = int(remainRMarbles)
        self.remainBMarbles = int(remainBMarbles)
        
class Action:
    def __init__(self, marble_color, marbles_taken):
        self.marble_color = marble_color
        self.marbles_taken = int(marbles_taken)
        self.utility = 0

def make_copy_state(state):   
    return State(state.remainRMarbles, state.remainBMarbles)

def take_action(action,state,current_player): # After taking an action, the game state changes. Configure the game state 
    # Take Action Message
    if((action.marble_color == "R") and (current_player == "computer")):
            print("Computer takes", action.marbles_taken, "red marbles.\n")    
    elif((action.marble_color == "B") and (current_player == "computer")):
            print("Computer takes", action.marbles_taken, "blue marble.\n")
    elif((action.marble_color == "R") and (current_player == "human")):
            print("You take", action.marbles_taken, "red marbles.\n")
    elif((action.marble_color == "B") and (current_player == "human")):
            print("You take", action.marbles_taken, "blue marbles.\n")

    # Things that will change: remaining marbles are the only thing that change from state to state
    if((action.marble_color == "B")): # Marble picked is blue
        state.remainBMarbles = state.remainBMarbles - action.marbles_taken
    else: # Marble picked is red
        state.remainRMarbles = state.remainRMarbles - action.marbles_taken

def print_marble_stacks(state):
    print("-------------------------------")
    print("Remaining Red Marbles: " , state.remainRMarbles)
    print("Remaining Blue Marbles: " , state.remainBMarbles)
    print("-------------------------------\n")

def is_integer(s):
    return s.isdigit()

def query_marble_color():
    marble_color = input("Choose Marble (R/B): ").rstrip()
    if(marble_color == "r"):
        marble_color = "R"    
    elif(marble_color == "b"):
        marble_color = "B"
    while((marble_color != "R") and (marble_color != "B")):
        marble_color = input("Choose Marble (R/B): ").rstrip()
        if(marble_color == "r"):
            marble_color = "R"        
        elif(marble_color == "b"):
            marble_color = "B"
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

def end_of_game(state,current_player,version):
    if((current_player == "computer") and (version == "standard")):
        print("You Won")
    elif((current_player == "human") and (version == "standard")):
        print("Game Over")
    elif((current_player == "computer") and (version == "misere")):
        print("Game Over")
    elif((current_player == "human") and (version == "misere")):
        print("You Won")

def successor_state(action, state): # works similarily like take_action(), used in the alpha-beta decision algorithm for the computer's decision. Returns the successor state after taking an action
    if(action.marble_color == "R"):
        successor = State(state.remainRMarbles - action.marbles_taken, state.remainBMarbles)    
    elif(action.marble_color == "B"):
        successor = State(state.remainRMarbles, state.remainBMarbles - action.marbles_taken)


    return successor

def possible_actions(state):
    actions = []

    # Case 1: 4 available options (R2, B2, R1, B1) <- The general case
    if((state.remainBMarbles>1) and (state.remainRMarbles>1)):
        actions.append(Action("R","2"))
        actions.append(Action("B","2"))
        actions.append(Action("R","1"))
        actions.append(Action("B","1"))
        
    # Case 2: 3 available options (R2, R1, B1) <- Edge case, there's only one blue marble left
    elif((state.remainBMarbles==1) and (state.remainRMarbles>1)):
        actions.append(Action("R","2"))
        actions.append(Action("R","1"))
        actions.append(Action("B","1"))
        
    # Case 3: 3 available options (B2, R1, B1) <- Edge case, there's only one red marble left
    elif((state.remainBMarbles>1) and (state.remainRMarbles==1)):
        actions.append(Action("B","2"))
        actions.append(Action("R","1"))
        actions.append(Action("B","1"))
        
    # Case 4: 2 available options (R1, B1) <Edge case, there's only one red and one blue marble left
    elif((state.remainBMarbles==1) and (state.remainRMarbles==1)):
        actions.append(Action("R","1"))
        actions.append(Action("B","1"))

    return actions

def successors(state):
    actionsList = possible_actions(state) # returns a list of possible actions and a corresponding list of successor states
    successorStateList = []
    for action in actionsList: 
        successorStateList.append(successor_state(action,state))
    return successorStateList

def utility(state):
    return (state.remainRMarbles * 2) + (state.remainBMarbles * 3)

def terminal_test(state):
    if ((state.remainRMarbles == 0) and (state.remainBMarbles == 0)):
        print(" Error in terminal_test(): remaining blue and red marbles are both zero", end=" ")
        return False
    if ((state.remainRMarbles == 0) or (state.remainBMarbles == 0)):
        return True
    else: 
        return False
# =====================================================================================================
def max_value(state, alpha, beta): 
    if (terminal_test(state) == True):
        return utility(state)
    v = -(sys.maxsize)

    successorStateList = successors(state)

    for s in successorStateList:
        v = max(v, min_value(s,alpha,beta))
        if(v>=beta):
            return v
        alpha = max(alpha,v)
        # alpha.value = max(alpha.value,v)
    
    return v

def min_value(state, alpha, beta):
    if (terminal_test(state) == True):
        return utility(state)
    v = sys.maxsize

    successorStateList = successors(state)

    for s in successorStateList:
        v = min(v, max_value(s,alpha,beta))
        if(v<=alpha):
            return v
        beta = min(beta,v)
        # beta.value = min(beta.value,v)
    
    return v  

def alpha_beta_decision(state):
    v = max_value(make_copy_state(state),-(sys.maxsize),sys.maxsize)
    print("Winning utiltity is", v)

    actionsList = possible_actions(make_copy_state(state)) # returns a list of possible actions for a given state
    utilities = []
    for action in actionsList:       
        utility = min_value(successor_state(action, make_copy_state(state)),-(sys.maxsize),sys.maxsize)
        utilities.append(utility)
        print("Utility for Action: " + str(action.marble_color) + str(action.marbles_taken)+ " is " + str(utility))

    for a, u, in zip(actionsList,utilities):
        if u == v:
            return a
# =====================================================================================================


def main():
    if(len(sys.argv)<3):
        print("Not enough arguments\n")
        sys.exit()

    arguments = sys.argv[1:] # Arguments passed: <num red> <num blue> <version> <first-player> <depth>.)

    state = State(arguments[0], arguments[1]) # Default state attributes set.

    if((arguments[2] == "standard") or (arguments[2] == "Standard")):
        version = "standard"
    elif((arguments[2] == "misere") or (arguments[2] == "Misere")):
        version = "misere"

    if((arguments[3] == "computer") or (arguments[3] == "Computer")):
        current_player = "computer"
    elif((arguments[3] == "human") or (arguments[3] == "Human")):
        current_player = "human"
    


    print("\n_______________________________Nim Game_______________________________")
    while((state.remainBMarbles>0) and (state.remainRMarbles>0)):
        if(current_player == "computer"):
            print("\n=====Computer=====")
            print_marble_stacks(state)
            action = alpha_beta_decision(make_copy_state(state))
            take_action(action, state, current_player)

            # NOTE: I may have to make a copy of the state before passing into alpha_beta_decision()

            current_player = "human"

        elif(current_player == "human"): #player turn
            print("\n=====Player=====")
            print_marble_stacks(state)

            marble_color = query_marble_color()
            marbles_taken = query_marbles_taken(state, marble_color)

            action = Action(marble_color, marbles_taken)

            take_action(action,state,current_player)
            current_player = "computer"
    end_of_game(state,current_player,version)



if __name__ == "__main__":
    main()
