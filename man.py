import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor


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
    for y in range(t.shape[0]):
        for x in range(t.shape[1]):
            color = color_interpolation(t[y][x]/iterations)
            image_test[y][x][0] = color[2]/255  # R
            image_test[y][x][1] = color[1]/255  # G
            image_test[y][x][2] = color[0]/255  # B
    return (x, y, image_test)


xstart = -2.5 + 1
ystart = -1.5 + 1
width = 4/4
height = 3/4

'''xstart = -2.5
ystart = -1.5
width = 4
height = 3'''

xsize = 4 * 100
ysize = 3 * 100

xcount = 1440 // xsize
ycount = 1080 // ysize

el_width = width / xcount
el_height = height / ycount

image = None
# image = mandelbrot(xstart, ystart, width, height, 200, 50)


# costam = worker(xstart, ystart, width, height, 50, 100)
# plt.imshow(costam[2])

results = []

with ThreadPoolExecutor() as executor:
    for y in range(ycount):
        image_line = None
        for x in range(xcount):
            future = executor.submit(worker, xstart + x * el_width, ystart + y *
                                     el_height, el_width, el_height, xsize // 4, 50)

            results.append(future)
            '''t = future.result()
            plt.imshow(t[2])
            plt.show()'''

    executor.shutdown(True)


'''for r in results:
    result = r.result()
    x = result[0]
    y = result[1]

    co_x = (x - xstart) / width * 1440
    co_y = (y - ystart) / height * 1080

    plt.figure()
    plt.imshow(result[2])  # , extent=(co_x, co_y, co_x + xsize, co_y + ysize))
plt.show()'''

image = None
#image = mandelbrot(xstart, ystart, width, height, 200, 50)
for y in range(ycount):
    image_line = None
    for x in range(xcount):
        #img_el = mandelbrot(xstart + x * elx, ystart + y * ely, elx, ely, 200, 50)
        img_el = results[x + y * 3].result()[2]

        if image_line is None:
            image_line = img_el
        else:
            image_line = np.concatenate((image_line, img_el), axis=1)

    if image is None:
        image = image_line
    else:
        image = np.concatenate((image, image_line))

plt.imshow(image)
plt.show()
#plt.imshow(image, cmap=plt.cm.twilight_shifted)
# plt.show()
# plt.savefig("Mandelbrot.png", dpi=250)
