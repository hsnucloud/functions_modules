# cubicSpline.py
# Import modules
import numpy as np

def cubicSplineInterpolate(t, y, z0, zn):
    """
    Solve for the cubic spline
    :param y: y array
    :param z0: initial z0
    :param zn: initial zn
    :return: cubic spline functions
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

    # Create cubic spline functions
    def cubicSpline(x):
        # Check the range of x
        for i in range(t.size-1):
            if t[i] <= x < t[i+1] or x == t[-1]:
                S = z[i]/6/h[i]*(t[i+1] - x)**3 + z[i+1]/6/h[i]*(x - t[i])**3 + (y[i+1]/h[i] - z[i+1]*h[i]/6)*(x - t[i]) + (y[i]/h[i] - z[i]*h[i]/6)*(t[i+1] - x)
        return S
    # Return cubic spline functions
    return cubicSpline