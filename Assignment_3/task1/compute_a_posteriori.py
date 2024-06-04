import sys

class h_i:
    def __init__(self, cherry, lime):
        self.cherry = float(cherry)
        self.lime = float(lime)


def build_P(): # Initial set of probabilities
    p1 = 0.1
    p2 = 0.2
    p3 = 0.4
    p4 = 0.2
    p5 = 0.1
    return [p1, p2, p3, p4, p5]


def build_H():
    h_1 = h_i(1.00000, 0.00000)
    h_2 = h_i(0.75000, 0.25000)
    h_3 = h_i(0.50000, 0.50000)
    h_4 = h_i(0.25000, 0.75000)
    h_5 = h_i(0.00000, 1.00000)

    return [h_1, h_2, h_3, h_4, h_5]

def build_Q():
    arguments = sys.argv[1:] # We want to process comand line arguments excluding the program name 
    arguments = arguments[:1] # We only want the argument that has the observations, which should be the argument after the program name. Everything else is trash
    # Q = [q_t(" ")] # Initial observation is empty
    Q = [] # Initial observation is empty
    if(len(arguments) != 0): # If we have observations, build an array containing our observations in order
        for char in arguments[0]:
            Q.append(char)
    return Q


def getProb(i,H,q):
    if (q == "C"):
        return H[i].cherry
    elif(q == "L"):
        return H[i].lime

def Normalize(P):
    sum = 0.0
    for p in range(len(P)):
        sum = sum + P[p]
    return sum


def main():
    P = build_P()
    H = build_H() # Array H contains h_1, ..., h_5. For each Class object h_i, the probabilities for either Cherry or Lime are defined as attributes
    Q = build_Q() # Array Q of characters ment to represent the T observations
    T = len(Q)

    with open("result.txt", "w") as file:
        file.write("Observation sequence ")

        # Printing Sequence Q
        file.write("Q: ")
        for q in Q:
            file.write(q+"")
        file.write("\n")

        file.write("Length of Q: " + str(T)+"\n\n")

        # We must go through and calculate the probability of each hypothesis i after t observations.
        for t in range(T):
            file.write("After Observation " + str(t + 1) + " = " + Q[t] + ":\n\n")

            for i in range(5):
                probability = getProb(i, H, Q[t])
                P[i] = probability * P[i]

            Psum = Normalize(P)

            for i in range(5):
                P[i] = P[i] / Psum

            for i in range(5):
                file.write("P(h" + str(i+1) + " | Q) = " + str(P[i]) + "\n")

            file.write("\n")

            probabilityNextC = 0.0
            for i in range(5):
                probabilityNextC = probabilityNextC + P[i] * getProb(i,H,'C')
            file.write("Probability that the next candy we pick will be C, given Q: " + str(probabilityNextC) + "\n")

            
            probabilityNextL = 0.0
            for i in range(5):
                probabilityNextL = probabilityNextL + P[i] * getProb(i,H,'L')
            file.write("Probability that the next candy we pick will be L, given Q: " + str(probabilityNextL) + "\n")

            file.write("\n")
    
if __name__ == "__main__":
    main()
