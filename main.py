import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import math
from man import *
from executor import *
from classic import Classic
import psutil
from time import perf_counter

xstart = -2.5 + 1.2
ystart = -1.5 + 1.05
width = 4/12
height = 3/12

'''xstart = -2.5
ystart = -1.5
width = 4
height = 3'''

xsize = 4 * 10 * 2
ysize = 3 * 10 * 2

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


def on_close(event):
    global parts
    parts = -1


plt.figure().canvas.mpl_connect('close_event', on_close)

plt.imshow(canvas)
plt.draw()
plt.pause(0.5)


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

#ex = Executor()
ex = Classic()

ex.schedule(queue, elements, xstart, ystart,
            el_width, el_height, xsize // 4, 200)

psutil.cpu_percent(percpu=True)
starttime = perf_counter()


parts = len(elements)
count = parts

while(parts > 0):
    result = queue.get()  # .result()
    parts -= 1

    x = result[0]
    y = result[1]

    co_x = (x - xstart) / width * image_width
    co_y = (y - ystart) / height * image_height

    blit(canvas, result[2], (int(co_y), int(co_x)))

    if queue.qsize() > 0:
        continue

    print(f"\r{count-parts}/{count}", end="")

    plt.clf()
    plt.imshow(canvas)

    plt.draw()
    plt.pause(0.01)

print()
print(psutil.cpu_percent(percpu=True))

endtime = perf_counter()

print(f"Time: {endtime - starttime}s")

ex.shutdown()

if parts >= 0:
    plt.ioff()
    plt.clf()
    plt.imshow(canvas)
    plt.show()

# plt.savefig("Mandelbrot.png", dpi=250)
