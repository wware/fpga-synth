# Python code to generate Postscript
# http://www.physics.emory.edu/~weeks/graphics/howtops1.html
# http://mahi.ucsd.edu/shearer/COMPCLASS/post.txt

import sys


class Point:
    def __init__(self, x=0., y=0.):
        self.x = x
        self.y = y

    def transform(self, xfm):
        return Point(xfm.scale * self.x + xfm.origin.x, xfm.scale * self.y + xfm.origin.y)

    def moveto(self, stream):
        stream.write('%f %f moveto ' % (self.x, self.y))

    def lineto(self, stream):
        stream.write('%f %f lineto ' % (self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def length(self):
        return (self.x * self.x + self.y * self.y) ** .5

    def dist(self, other):
        return (self - other).length()

    def __rmul__(self, other):
        if isinstance(other, Point):
            # dot product
            return self.x * other.x + self.y * other.y
        else:
            # scaling
            return Point(self.x * other, self.y * other)

    def parallel(self, other):
        # find the component of this 2-vector parallel to the arg 2-vector
        return ((self * other) / (other * other)) * other

    def perpendicular(self, other):
        # find the component of this 2-vector perpendicular to the arg 2-vector
        return self - self.parallel(other)

    def normal(self):
        return (1. / (self * self) ** .5) * self

    @classmethod
    def average(klas, *points):
        sum = klas()
        for p in points:
            sum = sum + p
        return (1. / len(points)) * sum


class Transformation:
    def __init__(self, scale, origin):
        self.scale = scale
        self.origin = origin

    def rescale(self, x):
        return Transformation(x * self.scale, self.origin)

    def translate(self, offset):
        return Transformation(self.scale, self.origin + offset)


class Path:
    def __init__(self, *points):
        self.points = points

    def transform(self, xfm):
        return apply(Path, tuple([p.transform(xfm) for p in self.points]))

    def render(self, stream):
        stream.write('newpath ')
        self.points[0].moveto(stream)
        for p in self.points[1:]:
            p.lineto(stream)
        stream.write('stroke ')


class Polygon(Path):
    def __init__(self, *points):
        self.points = list(points) + [points[0]]


class PostscriptPage:
    def __init__(self):
        self.paths = []

    def transform(self, xfm):
        page = PostscriptPage()
        page.paths = [path.transform(xfm) for path in self.paths]
        return page

    def add_path(self, *points):
        self.paths.append(apply(Path, points))

    def add_paths(self, *paths):
        [self.paths.append(path) for path in paths]

    def add_polygon(self, *points):
        self.paths.append(apply(Polygon, points))

    def render(self, stream=sys.stdout):
        stream.write('%!PS\n')
        [path.render(stream) for path in self.paths]
        stream.write('\nshowpage\n')


def sierpinski(p1, p2, p3, gap=0., depth=5, minsize=0.):
    if depth <= 0:
        return []
    if p1.dist(p2) < minsize and p1.dist(p3) < minsize and p2.dist(p3) < minsize:
        return []
    def edgepoint(u, v, w, gap=gap):
        h = 0.5 * gap * (w - u).perpendicular(v - u).normal()
        return Point.average(u, v) + h
    a, b, c = Point.average(p2, p3), Point.average(p1, p3), Point.average(p1, p2)
    return [
            Polygon(edgepoint(p1, p2, p3), edgepoint(p2, p3, p1), edgepoint(p3, p1, p2))
        ] + \
        sierpinski(p1, b, c, gap, depth-1, minsize) + \
        sierpinski(a, p2, c, gap, depth-1, minsize) + \
        sierpinski(a, b, p3, gap, depth-1, minsize)



PS_SPACE = Transformation(72, Point(36, 36))    # PS is 72 DPI, make a half-inch margin
