import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, Future
from queue import Queue
import math
from executor import Executor
from utils import *
from classic import Classic
import psutil
from time import perf_counter


def initPlot(image_height, image_width):
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
    return canvas


def draw(canvas):
    plt.clf()
    plt.imshow(canvas)
    plt.draw()
    plt.pause(0.01)


if __name__ == "__main__":

    xstart = -2.5 + 1.2
    ystart = -1.5 + 1.05
    width = 4/10
    height = width * 9/16

    '''xstart = -2.5
    ystart = -1.5
    width = 4
    height = 3'''

    xsize = 16 * 5
    ysize = 9 * 5

    image_width = 1920
    image_height = 1080

    xcount = image_width // xsize
    ycount = image_height // ysize

    el_width = width / xcount
    el_height = height / ycount

    canvas = initPlot(image_height, image_width)

    elements = order2D(xcount, ycount)

    queue = Queue()

    ex = Executor()
    #ex = Classic()

    ex.schedule(queue, elements, xstart, ystart,
                el_width, el_height, xsize // 16, 40)

    psutil.cpu_percent(percpu=True)
    starttime = perf_counter()

    parts = len(elements)
    count = parts

    while(parts > 0):
        result = queue.get()
        if isinstance(result, Future):
            result = result.result()
        parts -= 1

        x = result[0]
        y = result[1]

        co_x = (x - xstart) / width * image_width
        co_y = (y - ystart) / height * image_height

        blit(canvas, result[2], (int(co_y), int(co_x)))

        if queue.qsize() > 0:
            continue

        print(f"\r{count-parts}/{count}", end="")

        draw(canvas)

    print()
    print(psutil.cpu_percent(percpu=True))

    endtime = perf_counter()

    print(f"Time: {endtime - starttime}s")

    ex.shutdown()

    if parts >= 0:
        plt.ioff()
        draw(canvas)
        plt.show()

    # plt.savefig("Mandelbrot.png", dpi=250)
