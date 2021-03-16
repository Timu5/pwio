

def blit(dest, src, loc):
    sy, sx, _ = src.shape
    dx = sx + loc[1]
    dy = sy + loc[0]
    if dx >= dest.shape[1]:
        sx -= (dx - dest.shape[1])
    if dy >= dest.shape[0]:
        sy -= (dy - dest.shape[0])

    dest[loc[0]:loc[0]+sy, loc[1]:loc[1]+sx, :] = src[:sy, :sx, :]


def order2D(width, height):
    elements = []
    for y in range(height):
        for x in range(width):
            a = (y-height/2 + 0.5)
            b = (x-width/2 + 0.5)
            distance = max(abs(a), abs(b))
            elements.append((distance, x, y))
    elements.sort(key=lambda x: x[0])
    return elements
