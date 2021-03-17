import os
from queue import Queue
from threading import Thread

from executor import worker


class Classic:

    def __init__(self):
        self.elements = None
        self.queue = None
        self.thread_queue = Queue()

    def run(self, x, y, w, h, pd, i):
        result = worker(x, y, w, h, pd, i)
        self.queue.put(result)
        if self.thread_queue.not_empty:
            self.thread_queue.get().start()

    def schedule(self, queue, elements, xstart, ystart, el_width, el_height, pixel_density, iterations):
        self.queue = queue
        self.elements = elements

        for e in elements:
            d, x, y = e
            self.thread_queue.put(Thread(target=self.run, args=(xstart + x * el_width, ystart + y * el_height,
                                                                el_width, el_height, pixel_density, iterations)))

        for _ in range(min(os.cpu_count(), len(elements))):
            self.thread_queue.get().start()

    def shutdown(self):
        pass
