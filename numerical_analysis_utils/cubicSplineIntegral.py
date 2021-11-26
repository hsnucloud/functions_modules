# cubicSplineIntegral.py
# Import modules
import numpy as np

def cubicSplineIntegral(t, y, z0, zn):
    """
    Solve for the integral of cubic splines (integrating from t_0 to t_n)
    :param t: t array (knots)
    :param y: y array
    :param z0: initial z0
    :param zn: initial zn
    :return: Total integral of the cubic splines
    """
    h = np.diff(t) # h array
    u = np.zeros(shape=h.size) # u array
    for i in range(1, h.size):
        u[i] = 2*(h[i] + h[i-1])
    b = 6/h*np.diff(y) # b array
    v = np.zeros(shape=h.size) # v array
    for i in range(1, h.size):
        v[i] = b[i] - b[i-1]
    # print(h.size, h, u, b, v)
    z = np.zeros(shape=t.size) # initial z array
    z[0] = z0
    z[-1] = zn
    # Solve for z
    A = np.zeros(shape=(h.size-1, h.size-1))
    A[0][0] = u[1]
    A[0][1] = h[1]
    for i in range(1, h.size-2):
        A[i][i-1] = h[i]
        A[i][i] = u[i+1]
        A[i][i+1] = h[i+1]
    A[h.size-2][h.size-3] = h[h.size-2]
    A[h.size-2][h.size-2] = u[h.size-1]
    B = v[1:]
    # print(A, B, A.shape, B.shape)
    X = np.linalg.solve(A, B)
    # print(X)
    for i in range(1, h.size):
        z[i] = X[i-1]
    # print(z)

    # Integral of the cubic splines
    integral_S = 0
    for i in range(t.size-1):
        integral_S_i = h[i]/2*(y[i] + y[i+1]) - h[i]**3/24*(z[i] + z[i+1]) # Individual integral from t_i to t_i+1
        integral_S += integral_S_i

    # Return the accumulated value for the cubic spline integral
    return integral_S