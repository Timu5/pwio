import numpy as np
import matplotlib.pyplot as plt


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

elx = width/xcount
ely = height/ycount

a = np.array([[1,2], [1,2]])
b = np.array([[3,4], [3,4]])

c =  np.concatenate((a, b))
d =  np.concatenate((a, b), axis=1)


image = None
#image = mandelbrot(xstart, ystart, width, height, 200, 50)
for y in range(ycount):
    image_line = None
    for x in range(xcount):
        img_el = mandelbrot(xstart + x * elx, ystart + y * ely, elx, ely, 200, 50)

        if image_line is None:
            image_line = img_el
        else:
            image_line = np.concatenate((image_line, img_el), axis=1)

    if image is None:
        image = image_line
    else:
        image = np.concatenate((image, image_line))

plt.imshow(image, cmap=plt.cm.twilight_shifted)
plt.show()
#plt.savefig("Mandelbrot.png", dpi=250)
