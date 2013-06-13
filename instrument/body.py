# Python code to generate the shapes of the triangles forming the case of the instrument.
# Eventually this should crank out SVG, for the moment Postscript will do.
# http://www.physics.emory.edu/~weeks/graphics/howtops1.html
# http://mahi.ucsd.edu/shearer/COMPCLASS/post.txt

#SCALE = 72     # convert inches to units (for Postscript this is DPI)
SCALE = 0.2 * 72
ORIGIN = 1, 1
A = 24
B = 12

SQRT2 = 2 ** 0.5

def begin_page():
    print '%!PS'

def end_page():
    print 'showpage'

def draw(*pairs):

    def point(fmt, x, y):
        print fmt % (SCALE * (x + ORIGIN[0]), SCALE * (y + ORIGIN[0]))

    print 'newpath'
    pairs = list(pairs)
    x0, y0 = pairs.pop(0)
    point('%f %f moveto', x0, y0)
    for x, y in pairs:
        point('%f %f lineto', x, y)
    point('%f %f lineto', x0, y0)
    print 'stroke'


def linear_combo(a, x, b, y):
    return (a * x[0] + b * y[0], a * x[1] + b * y[1])


def sierpinski(x, y, z, transform, order):

    # TODO Specify a minimum gap between triangles so the thing doesn't
    # fall apart when you laser-cut it, and stays together afterwards.

    def avg(point1, point2):
        return linear_combo(0.5, point1, 0.5, point2)

    def sierpinski_recurse(x, y, z, order):
        a = avg(x, y)
        b = avg(y, z)
        c = avg(x, z)
        draw(a, b, c)
        if order > 0:
            sierpinski_recurse(x, a, c, order - 1)
            sierpinski_recurse(a, y, b, order - 1)
            sierpinski_recurse(c, b, z, order - 1)

    sierpinski_recurse(transform(x), transform(y), transform(z), order)

C = (A**2 - 0.5 * B**2)**.5 + B / SQRT2
D = (A**2 - B**2)**.5

begin_page()

draw((0, B / SQRT2),
     (B / SQRT2, 0),
     (B * SQRT2, B / SQRT2))

draw((0, B / SQRT2),
     (B, B / SQRT2),
     (B, D + B / SQRT2))

draw((2 * B, B / SQRT2),
     (B, B / SQRT2),
     (B, D + B / SQRT2))

a = (2 * B, B / SQRT2)
b = (2 * B - B / SQRT2, C)
c = (2 * B + B / SQRT2, C)
d = linear_combo(1, linear_combo(1./3, a, 1./3, b), 1./3, c)

draw(a, b, c)

def transform(point):
    h = 0.4
    return linear_combo(h, point, 1-h, d)

sierpinski(a, b, c, transform, 3)

end_page()
