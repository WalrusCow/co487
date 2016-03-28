from field import GF
G = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
P = (0xbac380aaefa5c656280bea4093ce7a06677f37c43bd121d5720b9ed2a6e1e2a5,
    0x5d88d4b08d21963b9a5c47ca9f875b05cb42237444727d5b42eb17a0f8d9dc40)
prime = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
hash = 0xc0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a
r = 0x32d80046e3257c4fe9b948e9b5b4d4aa4fcf05dff9bad6e056528f622f626b8c
s = 0x10e669184888d1427e0e3f0fd4d345cc7cec53f7be0688e58a7d858f3471c995

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
            if other.x is None and other.y is None:
                return Point(self.curve, self.x, self.y)
            if self.x is None and self.y is None:
                return Point(self.curve, other.x, other.y)
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
            return Point(self.curve, None, None)
        if n % 2 == 0:
            Q = (n / 2) * self
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
        return isinstance(o, ECC) and o.a == self.a and o.b == self.b

    def pt(self, x, y):
        return Point(self, self.gf(x), self.gf(y))


if __name__ == '__main__':
    f = GF(11)
    e = EllipticCurve(1, 6, f)
    print(e.pt(2, 4) + e.pt(5, 2))
    pt = e.pt(2, 4)
    print(pt + pt)
