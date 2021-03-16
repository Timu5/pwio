import numpy as np
from numpy.linalg import norm
from numba import jit


@jit(nopython=True, nogil=True)
def mandelbrot(x, y, w, h, pixel_density, iterations):
    d = pixel_density
    n = iterations
    r = 2.5  # escape radius (must be greater than 2)

    x = np.linspace(x, x + w, 16 * d + 1)
    y = np.linspace(y, y + h, 9 * d + 1)

    T = np.zeros((len(y), len(x)))

    for i, b in enumerate(y):
        for j, a in enumerate(x):
            c, z = a + b * 1j, 0j
            for k in range(n):
                if abs(z) >= r:
                    break
                z = z ** 2 + c
                T[i][j] = k + 1

    return T


@jit(nopython=True, nogil=True)
def color_interpolation(value):
    colormap = [
        (0.0, (0,   7, 100)),
        (0.16, (32, 107, 203)),
        (0.42, (237, 255, 255)),
        (0.6425, (255, 170, 0)),
        (0.8575, (0, 2, 0)),
        (1.0, (0, 2, 0))]
    prev = colormap[0]
    for cmap in colormap:
        if value < cmap[0]:
            distance = (value - prev[0]) / (cmap[0] - prev[0])
            r = distance * cmap[1][0] + (1 - distance) * prev[1][0]
            g = distance * cmap[1][1] + (1 - distance) * prev[1][1]
            b = distance * cmap[1][2] + (1 - distance) * prev[1][2]
            return (r, g, b)
        prev = cmap

    return colormap[-1][1]


@jit(nopython=True, nogil=True)
def colorize(matrix, iterations):
    # convert to image using some nice colors palete
    image = np.zeros(shape=(matrix.shape[0], matrix.shape[1], 3))
    for j in range(matrix.shape[0]):
        for i in range(matrix.shape[1]):
            color = color_interpolation(matrix[j][i]/iterations)
            image[j][i][0] = color[2]/255  # R
            image[j][i][1] = color[1]/255  # G
            image[j][i][2] = color[0]/255  # B
    return image
