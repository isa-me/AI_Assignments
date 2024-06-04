Name and ID: Isaac Medrano 1001884307
Programming Language: Python 3.10.12
Code Structure:
    I only had time to implement a function that could calculate the probability of a case where all variables are given a value and there are no dependencies.
    If you run my code with the following command: 
        python3 bnet.py Bt Ef At Jt Mt
    You should expect a value of: 
        0.0005910156
    Which matches the example problem in the bayesian_networks.pdf slides from class
    Example from the slides:
        P(B, not(E), A, JC, MC) = P(B) * P(not(E)) * P(A | B, not(E)) * P(JC | A) * P(MC | A) = 0.001 * 0.998 * 0.94 * 0.9 * 0.7 = 0.0005910156