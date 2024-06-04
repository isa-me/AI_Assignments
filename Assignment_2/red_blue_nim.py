import sys

class State:
    def __init__(self, remainRMarbles, remainBMarbles, version, depth):
        self.remainRMarbles = int(remainRMarbles)
        self.remainBMarbles = int(remainBMarbles)
        self.version = version
        self.depth = int(depth)
        
class Action:
    def __init__(self, marble_color, marbles_taken):
        self.marble_color = marble_color
        self.marbles_taken = int(marbles_taken)
        self.utility = 0

# =============================================================================================Functions For the Game Loop=============================================================================================
def print_intro(version): # Instructions on how to paly Nim
    print("______________________________________________________________________________________________________________________________")
    print("___________________________________________________________Nim Game___________________________________________________________")
    print("Welcome to Nim!\n\nInstructions:\nYou have a stack of red (R) marbles and another stack of blue (B) marbles.\nOn each turn you can take 1 or 2 marbles from either stack.")
    if(version == "standard"):
        print("Win Condition:\nYou are playing the " + version + " version of Nim. If on your turn either stack is empty, you lose.\n\n")
    elif(version == "misere"):
        print("Win Condition:\nYou are playing the " + version + " version of Nim. If on your turn either stack is empty, you win.\n\n")
    print("Score System:\nThe amount of points you win or lose is determined by the amount of marbles left at the end.\n\nRed marbles = 1 point\nBlue marbles - 2 points")
    print("______________________________________________________________________________________________________________________________")
    print("______________________________________________________________________________________________________________________________\n\n")


def config_init_state(arguments):
    # Command Line Argument Format: red_blue_nim.py <num-red> <num-blue> <version> <first-player> <depth>
    
    # Default Argument Values if not given or incorrect input
    first_player = "computer"
    version = "standard"
    depth = "0"

    if(len(arguments)>2): # User gave more than jsut the number of red and blue marbles.
        if(len(arguments)==3): # User gave one optional argument.
            if((arguments[2]=="human")or(arguments[2]=="Human")):
                first_player = "human"
            elif(arguments[2]=="misere")or(arguments[2]=="Misere"):
                version = "misere"
            elif(is_integer(arguments[2])):
                depth = arguments[2]
        elif(len(arguments)==4): # User gave atleast 2 optional arguments.
            if((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="human")or(arguments[3]=="Human")):
                version = "misere"
                first_player = "human"
            elif((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="computer")or(arguments[3]=="Computer")):  
                version = "misere"
            elif((arguments[2]=="standard")or(arguments[2]=="Standard") and (arguments[3]=="human")or(arguments[3]=="Human")):  
                first_player = "human"
            elif((arguments[2]=="misere")or(arguments[2]=="Misere") and is_integer(arguments[3])):
                version = "misere"
                depth = arguments[3]
            elif((arguments[2]=="human")or(arguments[2]=="Human") and is_integer(arguments[3])):
                first_player = "human"
                depth = arguments[3]
        elif(len(arguments)==5): # User gave all arguments.
            if(is_integer(arguments[4])):
                depth = arguments[4]
            if((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="human")or(arguments[3]=="Human")):
                version = "misere"
                first_player = human
            elif((arguments[2]=="misere")or(arguments[2]=="Misere") and (arguments[3]=="computer")or(arguments[3]=="Computer")):  
                version = "misere"
            elif((arguments[2]=="standard")or(arguments[2]=="Standard") and (arguments[3]=="human")or(arguments[3]=="Human")):  
                first_player = "human"
    return State(arguments[0], arguments[1], version, depth), first_player

def make_copy_state(state):   # Used to avoid passing by object reference inside the alpha beta prunning functions 
    return State(state.remainRMarbles, state.remainBMarbles, state.version, state.depth)

def take_action(action,state,current_player): # After taking an action, the game state changes. Configure the game state 
    # Take Action Message
    if((action.marble_color == "R") and (current_player == "computer")):
            print("\nComputer takes", action.marbles_taken, "red marbles.\n")    
    elif((action.marble_color == "B") and (current_player == "computer")):
            print("\nComputer takes", action.marbles_taken, "blue marble.\n")
    elif((action.marble_color == "R") and (current_player == "human")):
            print("\nYou take", action.marbles_taken, "red marbles.\n")
    elif((action.marble_color == "B") and (current_player == "human")):
            print("\nYou take", action.marbles_taken, "blue marbles.\n")

    # Things that will change: remaining marbles change in every game state
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

def query_marble_color(): # asks user for marble color
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
        print("You Won!\nYou scored:", str(state.remainRMarbles*2 + state.remainBMarbles*3), "points")
    elif((current_player == "human") and (version == "standard")):
        print("Game Over\nYou lost:", str(state.remainRMarbles*2 + state.remainBMarbles*3), "points")
    elif((current_player == "computer") and (version == "misere")):
        print("Game Over\nYou lost:", str(state.remainRMarbles*2 + state.remainBMarbles*3), "points")
    elif((current_player == "human") and (version == "misere")):
        print("You Won!\nYou scored:", str(state.remainRMarbles*2 + state.remainBMarbles*3), "points")

# =============================================================================================End of Game Loop Functions=============================================================================================


# =============================================================================================Alpha-Beta Prunning Functions=============================================================================================
def successor_state(action, state): # Returns a successor state after applying 'action' to 'state'
    if(action.marble_color == "R"):
        successor = State(state.remainRMarbles - action.marbles_taken, state.remainBMarbles, state.version, state.depth)    
    elif(action.marble_color == "B"):
        successor = State(state.remainRMarbles, state.remainBMarbles - action.marbles_taken, state.version, state.depth)
    return successor

def possible_actions(state): # Returns a list of possible actions at a given game state. Standard ordering:(R2,B2,R1,B1), Misere ordering: (B1,R1,B2,R2)
    actions = []

    if(state.version == "standard"):
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
    elif(state.version == "misere"):
        # Case 1: 4 available options (B1, R1, B2, R2) <- The general case
        if((state.remainBMarbles>1) and (state.remainRMarbles>1)):
            actions.append(Action("B","1"))
            actions.append(Action("R","1"))
            actions.append(Action("B","2"))
            actions.append(Action("R","2"))
        # Case 2: 3 available options (B1, R1, R2) <- Edge case, there's only one blue marble left
        elif((state.remainBMarbles==1) and (state.remainRMarbles>1)):
            actions.append(Action("B","1"))
            actions.append(Action("R","1"))
            actions.append(Action("R","2"))
        # Case 3: 3 available options (B1, R1, B2) <- Edge case, there's only one red marble left
        elif((state.remainBMarbles>1) and (state.remainRMarbles==1)):
            actions.append(Action("B","1"))
            actions.append(Action("R","1"))
            actions.append(Action("B","2"))
        # Case 4: 2 available options (B1, R1) <Edge case, there's only one red and one blue marble left
        elif((state.remainBMarbles==1) and (state.remainRMarbles==1)):
            actions.append(Action("B","1"))
            actions.append(Action("R","1"))
    return actions

def successors(state): # returns a list of possible successor states
    actionsList = possible_actions(state) 
    successorStateList = []
    for action in actionsList: 
        successorStateList.append(successor_state(action,state))
    return successorStateList

def utility(state, player):
    # Utility Function for the standard version
    if((player == "human") and (state.version == "standard")): # Computer won, the more favorable case is the one where the human has less "losing points". This is because the objective of the computer is to win with the most possible points, not win and spite the losing opponent with the most possible "losing poits"
        if(state.remainRMarbles > state.remainBMarbles):
            return 6
        elif(state.remainRMarbles == state.remainBMarbles):
            return 5
        elif(state.remainRMarbles < state.remainBMarbles):
            return 4
    elif((player == "computer") and (state.version == "standard")): # Computer lost, the more favorable case is the one where the computer has the least "losing points"
        if(state.remainRMarbles > state.remainBMarbles):
            return 3
        elif(state.remainRMarbles == state.remainBMarbles):
            return 2
        elif(state.remainRMarbles < state.remainBMarbles):
            return 1
    # Utility for the misere version
    elif((player == "computer") and (state.version == "misere")): #Computer won, the more favorable case is the one where the computer has the most "Winning points"
        if(state.remainRMarbles < state.remainBMarbles):
            return 6
        elif(state.remainRMarbles == state.remainBMarbles):
            return 5
        elif(state.remainRMarbles > state.remainBMarbles):
            return 4
    elif((player == "human") and (state.version == "misere")): # Computer lost, the more favorable case is the one where the human is merciful and gives the computer the least possible "losing points"
        if(state.remainRMarbles > state.remainBMarbles):
            return 3
        elif(state.remainRMarbles == state.remainBMarbles):
            return 2
        elif(state.remainRMarbles < state.remainBMarbles):
            return 1

def terminal_test(state):
    if ((state.remainRMarbles == 0) and (state.remainBMarbles == 0)):
        print(" Error in terminal_test(): remaining blue and red marbles are both zero", end=" ")
        return False
    if ((state.remainRMarbles == 0) or (state.remainBMarbles == 0)):
        return True
    else: 
        return False

def max_value(state, alpha, beta): 
    if (terminal_test(state) == True):
        return utility(state,"computer")
    v = -(sys.maxsize)

    successorStateList = successors(state)

    for s in successorStateList:
        v = max(v, min_value(s,alpha,beta))
        if(v>=beta):
            return v
        alpha = max(alpha,v)
    
    return v

def min_value(state, alpha, beta):
    if (terminal_test(state) == True):
        return utility(state,"human")
    v = sys.maxsize

    successorStateList = successors(state)

    for s in successorStateList:
        v = min(v, max_value(s,alpha,beta))
        if(v<=alpha):
            return v
        beta = min(beta,v)
    
    return v  

def depth_limited_max_value(state, alpha, beta,depth): 
    if ((terminal_test(state) == True) or (depth==0)): #cutoff test
        return utility(state,"computer")
    v = -(sys.maxsize)

    successorStateList = successors(state)

    for s in successorStateList:
        v = max(v, depth_limited_min_value(s,alpha,beta,depth-1))
        if(v>=beta):
            return v
        alpha = max(alpha,v)
    
    return v

def depth_limited_min_value(state, alpha, beta, depth):
    if ((terminal_test(state) == True) or (depth==0)):
        return utility(state,"human")
    v = sys.maxsize

    successorStateList = successors(state)

    for s in successorStateList:
        v = min(v, depth_limited_max_value(s,alpha,beta,depth-1))
        if(v<=alpha):
            return v
        beta = min(beta,v)
    
    return v  

def alpha_beta_decision(state):
    if(state.depth == 0):
        v = max_value(make_copy_state(state),-(sys.maxsize),sys.maxsize)
        print("Winning utiltity is", v)

        actionsList = possible_actions(make_copy_state(state)) # returns a list of possible actions for a given state
        utilities = []
        for action in actionsList:       
            utility = min_value(successor_state(action, make_copy_state(state)),-(sys.maxsize),sys.maxsize)
            utilities.append(utility)
            print("Utility for Action: " + str(action.marble_color) + str(action.marbles_taken)+ " is " + str(utility))
        print("")

        for a, u, in zip(actionsList,utilities):
            if u == v:
                return a
    elif(state.depth > 0):
        depth = state.depth
        v = depth_limited_max_value(make_copy_state(state),-(sys.maxsize),sys.maxsize, depth + 0)
        print("Winning utiltity is", v)

        actionsList = possible_actions(make_copy_state(state)) # returns a list of possible actions for a given state
        utilities = []
        for action in actionsList:       
            utility = depth_limited_min_value(successor_state(action, make_copy_state(state)),-(sys.maxsize),sys.maxsize, depth - 1)
            utilities.append(utility)
            print("Utility for Action: " + str(action.marble_color) + str(action.marbles_taken)+ " is " + str(utility))
        print("")

        for a, u, in zip(actionsList,utilities):
            if u == v:
                return a
# =============================================================================================End of Alpha-Beta Prunning Functions=============================================================================================

def main():
    if(len(sys.argv)<3):
        print("Not enough arguments\n")
        sys.exit()

    arguments = sys.argv[1:]
    state, current_player = config_init_state(arguments)
    
    print_intro(state.version)
    while((state.remainBMarbles>0) and (state.remainRMarbles>0)): # Game Loop: Game ends when either marble stack is empty
        if(current_player == "computer"): # Computer Turn
            print("\n===============================Computer===============================")
            print_marble_stacks(state)
            action = alpha_beta_decision(make_copy_state(state))
            take_action(action, state, current_player)
            current_player = "human"
            print("========================================================================")


        elif(current_player == "human"): # Human Turn
            print("\n================================Player================================")
            print_marble_stacks(state)

            marble_color = query_marble_color()
            marbles_taken = query_marbles_taken(state, marble_color)

            action = Action(marble_color, marbles_taken)

            take_action(action,state,current_player)
            current_player = "computer"
            print("========================================================================")
    print_marble_stacks(state)
    end_of_game(state,current_player,state.version)



if __name__ == "__main__":
    main()
