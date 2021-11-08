# polyInterpolation.py
# Import modules
import numpy as np

def LagrangePolynomial(x_data, y_data, x):
    n = len(x_data)
    P = 0
    for k in range(n):
        l_k = 1
        for i in range(n):
            if i != k:
                l_k = ((x - x_data[i])/(x_data[k] - x_data[i]))*l_k
        P += y_data[k]*l_k
    return P