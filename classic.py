from executor import worker


class Classic:

    def __init__(self):
        pass

    def schedule(self, queue, elements, xstart, ystart, el_width, el_height, pixel_density, iterations):
        # queue - place to put calculation result
        # elements - list of elements for which multi-thread calculations should be done
        # remaining arguments are passed to worker() function

        # use worker() function for calculation
        # worker() arguments: xstart + x * el_width, ystart + y * el_height, el_width, el_height, pixel_density, iterations
        # where x and y is second and third tuple element from "elements" array eg. elements[0][1] <- x, elements[0][2] <- y

        # return value from worker() need to be directly put into "queue"

        # spawn at least as many thread as logical cores

        pass

    def shutdown(self):
        pass
