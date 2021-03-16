import numpy as np
from concurrent.futures import ThreadPoolExecutor, Future
from queue import Queue
import math
from executor import Executor
from utils import *
from classic import Classic
import psutil
from time import perf_counter
import cv2


def draw(canvas):
    imscaled = cv2.resize(canvas, (1920//2, 1080//2))
    cv2.imshow("Mandelbrot", imscaled)


if __name__ == "__main__":

    gui = True
    fps = 30

    xstart = -2.5 + 1.2
    ystart = -1.5 + 1.05
    width = 4/10
    height = width * 9/16

    '''xstart = -2.5
    ystart = -1.5
    width = 4
    height = 3'''

    xsize = 16 * 10 * 2 * 2
    ysize = 9 * 10 * 2 * 2

    image_width = 1920 * 2 * 2
    image_height = 1080 * 2 * 2

    xcount = image_width // xsize
    ycount = image_height // ysize

    el_width = width / xcount
    el_height = height / ycount

    canvas = np.zeros(shape=(image_height, image_width, 3))
    canvas.fill(1.0)

    if gui:
        draw(canvas)
        cv2.waitKey(1)

    elements = order2D(xcount, ycount)

    queue = Queue()

    #ex = Executor()
    ex = Classic()

    psutil.cpu_percent(percpu=True)
    starttime = perf_counter()

    ex.schedule(queue, elements, xstart, ystart,
                el_width, el_height, xsize // 16, 300)

    parts = len(elements)
    count = parts

    lasttime = starttime

    while parts > 0:
        result = queue.get()
        if isinstance(result, Future):
            result = result.result()
        parts -= 1

        x = result[0]
        y = result[1]

        co_x = (x - xstart) / width * image_width
        co_y = (y - ystart) / height * image_height

        blit(canvas, result[2], (int(co_y), int(co_x)))

        time = perf_counter()
        if time - lasttime < 1 / fps:
            continue

        lasttime = time
        print(f"\r{count-parts}/{count}", end="")

        if gui:
            draw(canvas)
            cv2.waitKey(1)

    print()
    print(psutil.cpu_percent(percpu=True))

    endtime = perf_counter()

    print(f"Time: {endtime - starttime}s")

    ex.shutdown()

    if gui:
        draw(canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
