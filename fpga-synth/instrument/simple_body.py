# Simplified body, this is just two parallel triangles

import pslib

A = 24
B = 16

page = pslib.PostscriptPage()

a = pslib.Point(0, 0)
b = pslib.Point(B, 0)
c = pslib.Point(B / 2, A)
d = pslib.Point.average(a, b, c)

page.add_polygon(a, b, c)

h = 0.4
a1 = h * a + (1 - h) * d
b1 = h * b + (1 - h) * d
c1 = h * c + (1 - h) * d

def keyboard():
    holes = []
    m, n = 0.7, 0.375
    m, n = 0.7, 0.4
    for (a, blo, bhi) in ((0, 1, 7), (1, 0, 12), (2, 5, 17), (3, 10, 22), (4, 15, 21)):
        for b in range(blo, bhi):
            x = 14 + m * a - n * b
            y = 1.5 + m * b + n * a
            holes.append(pslib.Hole(pslib.Point(x, y), 0.1))
    return holes

[page.add_path(h) for h in keyboard()]

apply(page.add_paths, pslib.sierpinski(a1, b1, c1, depth=3, gap=0.4))

# here's the back
# a = pslib.Point(3 * B / 2, A)
# page.add_polygon(a, b, c)

# page.transform(pslib.PS_SPACE.rescale(0.35)).render()
page.transform(pslib.PS_SPACE).render()
