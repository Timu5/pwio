import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from man import mandelbrot, colorize
import os


def worker(x, y, w, h, pixel_density, iterations):
    t = mandelbrot(x, y, w, h, pixel_density, iterations)
    image = colorize(t, iterations)
    return (x, y, image, t)


class Executor:

    def __init__(self):
        self.queue = None
        self.executor = None

    def worker_finished(self, future):
        self.queue.put(future)

    def schedule(self, queue, elements, xstart, ystart, el_width, el_height, pixel_density, iterations):
        self.queue = queue
        self.executor = ThreadPoolExecutor(max_workers=os.cpu_count())
        for e in elements:
            d, x, y = e
            future = self.executor.submit(worker, xstart + x * el_width, ystart + y *
                                          el_height, el_width, el_height, pixel_density, iterations)
            future.add_done_callback(self.worker_finished)

    def shutdown(self):
        self.executor.shutdown(wait=False, cancel_futures=True)
