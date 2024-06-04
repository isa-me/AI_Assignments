import sys

# B = ['0.001'] # Probabililty
B = [0.001] # Probabililty

# E = ['0.002'] # Probability
E = [0.002] # Probability

# A = [   ['t','t','f','f'], # Tuples for B
#             ['t','f','t','f'], # Tuples for E
#             ['0.95','0.94','0.29','0.001']] # Tuples for Probability
AB = [True,True,False,False]
AE = [True,False,True,False]
A = [0.95,0.94,0.29,0.001]

# J = [   ['t','f'], # Tuples for A
#                 ['0.90','0.05']] # Tuples for Probability 
JA = [True,False] # Tuples for A
J = [0.90,0.05]# Tuples for Probability 

# M = [   ['t','f'], # Tuples for A
#                 ['0.70','0.01']] # Tuples for Probability 
MA = [True,False] # Tuples for A
M =  [0.70,0.01] # Tuples for Probability 

class Bayesian:
    def __init__(self,Y, E, given):
        self.Y = Y
        self.E = E
        self.given = given
    def computeProbability(self, b, e, a, j, m): # calculates the probability of a case where all variables are given a value and there are no dependencies.
        #
        result = 1.0
        if(b==True):
            result = result * B[0]
        else:
            result = result * (1-B[0])

        if(e==True):
            result = result * E[0]
        else:
            result = result * (1-E[0])

        for i in range(4):
            if(AB[i] == b and AE[i] == e):
                if(a==True):
                    result = result * A[i]
                else:
                    result = result * (1-A[i])

        for i in range(2):
            if(JA[i] == a):
                if(j==True):
                    result = result * J[i]
                else:
                    result = result * (1-J[i])

        for i in range(2):
            if(MA[i] == a):
                if(m==True):
                    result = result * M[i]
                else:
                    result = result * (1-M[i])
        return result


def proccess_args():
    arguments = sys.argv[1:] # We want to process comand line arguments excluding the program name 
    arguments = arguments[:6] # There are 1-6 arguments that are possible
    Y = [] # Yield Variables
    E = [] # Evidence Variables
    givenFlag = False
    for a in arguments:
        if(a == "given" or a == "Given"):
            givenFlag == True
        elif(givenFlag == False):
            Y.append(a)
        elif(givenFlag == True):
            E.append(a)
    return Y, E, givenFlag



def main():
    Y,E,givenFlag = proccess_args()
    BN = Bayesian(Y,E,givenFlag)

    if(len(Y) == 5 and givenFlag == False): # All variables are given a value and there are no dependencies
        b = False
        e = False
        a = False
        j = False
        m = False
        for y in Y:
            char_array = [char for char in y]
            if (char_array[0] == 'B' and char_array[1] == "t"):
                b = True
            if (char_array[0] == 'E' and char_array[1] == "t"):
                e = True
            if (char_array[0] == 'A' and char_array[1] == "t"):
                a = True
            if (char_array[0] == 'J' and char_array[1] == "t"):
                j = True
            if (char_array[0] == 'M' and char_array[1] == "t"):
                m = True
        result = BN.computeProbability(b, e, a, j, m)
        print(str(result))

    elif(len(Y) < 5 and given == False): # No dependecies, Only some of the variables have values. Need to enumerate
        H = [] # array for hidden variables
        for y in range(len(Y))

    # elif(givenFlag == True): # Dependecies. Either side will be incomplete

    

    
if __name__ == "__main__":
    main()