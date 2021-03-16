import numpy as np


def mandelbrot(x, y, w, h, pixel_density, iterations):
    d = pixel_density
    n = iterations
    r = 2.5  # escape radius (must be greater than 2)

    x = np.linspace(x, x + w, 16 * d + 1)
    y = np.linspace(y, y + h, 9 * d + 1)

    A, B = np.meshgrid(x, y)
    C = A + B * 1j

    Z = np.zeros_like(C)
    T = np.zeros(C.shape)

    for k in range(n):
        M = abs(Z) < r  # probe number
        Z[M] = Z[M] ** 2 + C[M]  # Z(n+1) = Zn^2 + p
        T[M] = k + 1

    return T


colormap = [
    (0.0, (0,   7, 100)),
    (0.16, (32, 107, 203)),
    (0.42, (237, 255, 255)),
    (0.6425, (255, 170, 0)),
    (0.8575, (0, 2, 0)),
    (1.0, (0, 2, 0))]


def color_interpolation(value):
    prev = None
    for cmap in colormap:
        if value < cmap[0]:
            distance = (value - prev[0]) / (cmap[0] - prev[0])
            r = distance * cmap[1][0] + (1 - distance) * prev[1][0]
            g = distance * cmap[1][1] + (1 - distance) * prev[1][1]
            b = distance * cmap[1][2] + (1 - distance) * prev[1][2]
            return [r, g, b]
        prev = cmap

    return colormap[-1][1]


def colorize(matrix, iterations):
    # convert to image using some nice colors palete
    image = np.zeros(shape=(matrix.shape[0], matrix.shape[1], 3))
    for j in range(matrix.shape[0]):
        for i in range(matrix.shape[1]):
            color = color_interpolation(matrix[j][i]/iterations)
            image[j][i][0] = color[0]/255  # R
            image[j][i][1] = color[1]/255  # G
            image[j][i][2] = color[2]/255  # B
    return image
