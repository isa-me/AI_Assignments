Name and ID: Isaac Medrano 1001884307
Programming Language: Python 3.10.12
Code Structure:
    1. Object class that has the probabilities for either cherry or lime depending on the bag type (h_1, ..., h_5)
    2. Function that builds the initial set of Probabilities (the known priors for each h_i)
    3. Function that builds the set of h_i with the probabilities for either cherry or lime hardcoded
    4. Function that builds an array of characters out of the command line argument containing the observations
    5. A function that takes a character 'q' from array 'Q'. Q holds the observation sequence and q is either 'L' or 'C'. This function fetches the probability from H[i] for either 'C' or 'L'.
    6. The Normalize function just summarizes all the float values in an array
    7. Main function that handles the computations for the probability of each hypothesis i after t observations.

How to Run Code:
    In the same directory that has compute_a_posteriori.py, run the following command

    python3 compute_a_posteriori.py <Observation_Sequence>

    replace <Observation_Sequence> with any string made up of L and C (e.g. LCLCLCLLCLCLLLC)

