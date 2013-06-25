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

apply(page.add_paths, pslib.sierpinski(a1, b1, c1, depth=3, gap=0.5))

# here's the back
a = pslib.Point(3 * B / 2, A)
page.add_polygon(a, b, c)

page.transform(pslib.PS_SPACE.rescale(0.2)).render()
