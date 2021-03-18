from numba import jit


@jit(nopython=True, nogil=True)
def blit(dest, src, loc):
    sy, sx, _ = src.shape
    dx = sx + loc[1]
    dy = sy + loc[0]
    if dx >= dest.shape[1]:
        sx -= dx - dest.shape[1]
    if dy >= dest.shape[0]:
        sy -= dy - dest.shape[0]

    dest[loc[0] : loc[0] + sy, loc[1] : loc[1] + sx, :] = src[:sy, :sx, :]


def order2D(m, n):
    k = 0  # row
    l = 0  # column
    elements = []

    while k < m and l < n:

        for i in range(l, n):
            elements.append((0, k, i))
        k += 1

        for i in range(k, m):
            elements.append((0, i, n - 1))
        n -= 1

        if k < m:
            for i in range(n - 1, (l - 1), -1):
                elements.append((0, m - 1, i))
            m -= 1

        if l < n:
            for i in range(m - 1, k - 1, -1):
                elements.append((0, i, l))
            l += 1

    el = elements[::-1]
    return el
