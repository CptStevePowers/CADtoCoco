import numpy as np


def point_sphere(n=10, r=1): #TODO: add random seed?
    from numpy import pi, cos, sin, arccos, arange
    indices = arange(0, n, dtype=float) + 0.5

    phi = arccos(1 - 2*indices/n)
    theta = pi * (1 + 5**0.5) * indices

    x, y, z = cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)
    x, y, z = x * r, y * r, z * r
    def round_3(x): return round(x, 3)
    x = np.fromiter(map(round_3, x), dtype=float)
    y = np.fromiter(map(round_3, y), dtype=float)
    z = np.fromiter(map(round_3, z), dtype=float)

    points = []
    for i in range(n):
        points.append((x[i], y[i], z[i]))
    return points


def test_point_sphere(verbose=False):
    import mpl_toolkits.mplot3d
    import matplotlib.pyplot as pp
    import random
    import math

    num_pts = random.randint(10,3000)
    r = random.randint(1, 10)
    print('### Testing point_sphere(n={0}, r={1})'.format(num_pts, r))
    points = point_sphere(n=num_pts, r=r)

    x = [i[0] for i in points]
    y = [i[1] for i in points]
    z = [i[2] for i in points]


    sample = random.sample(points, round(len(points) / 10))

    for p in sample:
        p2 = np.array(p)
        l = np.linalg.norm(p2)
        l = round(l, 2)
        assert l <= r, "Point {0} not on sphere. Length: {1} Expected: {2}".format(
            p, l, r)

    if verbose:
        pp.figure().add_subplot(111, projection='3d').scatter(x, y, z)
        pp.show()


if __name__ == '__main__':
    test_point_sphere()
    print('\nAll passed.\n')
