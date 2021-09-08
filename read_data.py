# Read data file and return x y columns
def readXYData(filename):
    if filename.endswith(".dat"):
        x, y = np.loadtxt(filename, unpack=True, usecols=(0, 1))
        return x, y
    elif filename.endswith(".txt"):
        x, y = np.loadtxt(filename, unpack=True, usecols=(0, 1))
        return x, y
    elif filename.endswith(".csv"):
        x, y = np.loadtxt(filename, delimiter=',', unpack=True, usecols=(0, 1))
        return x, y
    else:
        x = None
        y = None
        return x, y