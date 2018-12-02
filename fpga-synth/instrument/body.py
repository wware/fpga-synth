import pslib

page = pslib.PostscriptPage()

A = 24
B = 12

SQRT2 = 2 ** 0.5

C = (A**2 - 0.5 * B**2)**.5 + B / SQRT2
D = (A**2 - B**2)**.5

page.add_polygon(pslib.Point(0, B / SQRT2),
                 pslib.Point(B / SQRT2, 0),
                 pslib.Point(B * SQRT2, B / SQRT2))

page.add_polygon(pslib.Point(0, B / SQRT2),
                 pslib.Point(B, B / SQRT2),
                 pslib.Point(B, D + B / SQRT2))

page.add_polygon(pslib.Point(2 * B, B / SQRT2),
                 pslib.Point(B, B / SQRT2),
                 pslib.Point(B, D + B / SQRT2))

a = pslib.Point(2 * B, B / SQRT2)
b = pslib.Point(2 * B - B / SQRT2, C)
c = pslib.Point(2 * B + B / SQRT2, C)
d = pslib.Point.average(a, b, c)

page.add_polygon(a, b, c)

h = 0.4
a1 = h * a + (1 - h) * d
b1 = h * b + (1 - h) * d
c1 = h * c + (1 - h) * d

apply(page.add_paths, pslib.sierpinski(a1, b1, c1, depth=3, gap=0.5))

page.transform(pslib.PS_SPACE.rescale(0.2).translate(pslib.Point(1, 1))).render()
