import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import math


def mandelbrot(x, y, w, h, pixel_density, iterations):
    d = pixel_density
    n = iterations
    # d, n = 200, 50  # pixel density & number of iterations
    r = 2.5  # escape radius (must be greater than 2)

    x = np.linspace(x, x + w, 4 * d + 1)
    y = np.linspace(y, y + h, 3 * d + 1)

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
            return (r, g, b)
        prev = cmap

    return colormap[-1][1]


def worker(x, y, w, h, pixel_density, iterations):
    t = mandelbrot(x, y, w, h, pixel_density, iterations)
    # convert to image using some nice colors palete
    image_test = np.zeros(shape=(t.shape[0], t.shape[1], 3))
    for j in range(t.shape[0]):
        for i in range(t.shape[1]):
            color = color_interpolation(t[j][i]/iterations)
            image_test[j][i][0] = color[0]/255  # R
            image_test[j][i][1] = color[1]/255  # G
            image_test[j][i][2] = color[2]/255  # B
    return (x, y, image_test)


xstart = -2.5 + 1.2
ystart = -1.5 + 1.05
width = 4/12
height = 3/12

'''xstart = -2.5
ystart = -1.5
width = 4
height = 3'''

xsize = 4 * 10 * 5 * 2
ysize = 3 * 10 * 5 * 2

image_width = 400 * 5
image_height = 300 * 5

xcount = image_width // xsize
ycount = image_height // ysize

el_width = width / xcount
el_height = height / ycount

plt.ion()
plt.show()

canvas = np.zeros(shape=(image_height, image_width, 3))
canvas.fill(1.0)

plt.imshow(canvas)
plt.draw()
plt.pause(0.01)


# TODO: optimize this routine
def blit(dest, src, loc):
    y, x = loc
    sy, sx, _ = src.shape
    dx = sx + x
    dy = sy + y
    if dx >= dest.shape[1]:
        sx -= (dx - dest.shape[1])
    if dy >= dest.shape[0]:
        sy -= (dy - dest.shape[0])
    for j in range(sy):
        dest[j+loc[0]][loc[1]:loc[1]+sx] = src[j][0:sx]


elements = []
for y in range(ycount):
    for x in range(xcount):
        a = abs(y-ycount//2)
        b = abs(x-xcount//2)
        distance = max(a, b)
        elements.append((distance, x, y))
elements.sort(key=lambda x: x[0])


queue = Queue()


def worker_finished(future):
    queue.put(future.result())


parts = 0
executor = ThreadPoolExecutor()
for e in elements:
    x = e[1]
    y = e[2]
    future = executor.submit(worker, xstart + x * el_width, ystart + y *
                             el_height, el_width, el_height, xsize // 4, 120)
    future.add_done_callback(worker_finished)
    parts += 1

while(parts > 0):
    result = queue.get()

    x = result[0]
    y = result[1]

    co_x = (x - xstart) / width * image_width
    co_y = (y - ystart) / height * image_height

    blit(canvas, result[2], (int(co_y), int(co_x)))
    plt.clf()
    plt.imshow(canvas)

    plt.draw()
    plt.pause(0.01)

    parts -= 1

executor.shutdown()

plt.ioff()
plt.show()

# plt.savefig("Mandelbrot.png", dpi=250)
