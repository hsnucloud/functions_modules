"""
The class of poly1d function:
input a list of coefficients
output the function value (y), curvature, and radius of curvature
"""


class poly1d_function:
    def __init__(self, *args):
        self.coef_number = len(*args)
        self.coefs = args[0]

    def value(self, x):
        v = 0
        for i in reversed(range(self.coef_number)):
            v += self.coefs[i]*x**(self.coef_number - 1 - i)
        return v

    def value_1st_diff(self, x):
        v = 0
        for i in reversed(range(self.coef_number - 1)):
            v += self.coefs[i]*x**(self.coef_number - 2 - i)*(self.coef_number - 1 - i)
        return v

    def value_2nd_diff(self, x):
        v = 0
        for i in reversed(range(self.coef_number - 2)):
            v += self.coefs[i] * x ** (self.coef_number - 3 - i)*(self.coef_number - 2 - i)*(self.coef_number - 1 - i)
        return v

    def curvature(self, x):
        kappa = abs(self.value_2nd_diff(x))/(1+self.value_1st_diff(x)**2)**1.5
        return kappa

    def radius_of_curvature(self, x):
        rof = 1/self.curvature(x)
        return rof

