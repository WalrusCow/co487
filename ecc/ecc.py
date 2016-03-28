from field import GF

class Point():
    def __init__(self, curve, x, y):
        self.curve = curve
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return (isinstance(other, Point) and
                self.curve == other.curve and
                self.x == other.x and
                self.y == other.y)

    def __add__(self, other):
        if self.curve != other.curve:
            raise TypeError('Cannot add two points of different curves!')

        try:
            if other.x == 0 and other.y == 0:
                return Point(self.curve, self.x, self.y)
            if self.x == 0 and self.y == 0:
                return Point(self.curve, other.x, other.y)
            if self.x == other.x and self.y == (-1 * other.y):
                return Point(self.curve, 0, 0)
            if self == other:
                m = (3 * (self.x * self.x) + self.curve.a) / (2 * self.y)
            else:
                m = (other.y - self.y) / (other.x - self.x)
            sum_x = m * m - self.x - other.x
            sum_y = -1 * (m * (sum_x - self.x) + self.y)
            return Point(self.curve, sum_x, sum_y)

        except Exception as e:
            raise TypeError('Invalid addition: ' + str(e))

    def __rmul__(self, n):
        if not isinstance(n, int):
            raise ValueError('{} is not an int'.format(str(n)))

        if n == 0:
            return Point(self.curve, 0, 0)
        if n % 2 == 0:
            Q = (n >> 1) * self
            return Q + Q
        else:
            return ((n - 1) * self) + self

class EllipticCurve():
    def __init__(self, a, b, gf):
        ''' Elliptic curve of the form y^2 - x^3 + ax + b. '''
        self.a = a
        self.b = b
        self.gf = gf

    def __eq__(self, o):
        return isinstance(o, EllipticCurve) and o.a == self.a and o.b == self.b

    def pt(self, x, y):
        return Point(self, self.gf(x), self.gf(y))

if __name__ == '__main__':
    f = GF(11)
    e = EllipticCurve(1, 6, f)
    print(e.pt(2, 4) + e.pt(5, 2))
    pt = e.pt(2, 4)
    print(pt + pt)
