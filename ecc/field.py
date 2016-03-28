class ModularNumber():
    def __init__(self, gf, value):
        self.gf = gf
        self.value = value % gf.size

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        return (isinstance(other, ModularNumber) and
                self.gf == other.gf and
                self.value == other.value)

    def __gt__(self, other):
        if isinstance(other, int):
            return self.value > other
        return self.value > other.value

    def __add__(self,  other):
        if isinstance(other, int):
            return self + ModularNumber(self.gf, other)
        if self.gf != other.gf:
            raise TypeError('Field sizes do not match')
        return ModularNumber(self.gf, self.value + other.value)

    def __sub__(self, other):
        if isinstance(other, int):
            return self - ModularNumber(self.gf, other)
        if self.gf != other.gf:
            raise TypeError('Field sizes do not match')
        return ModularNumber(self.gf, self.value - other.value)

    def __mul__(self, other):
        if isinstance(other, int):
            return self * ModularNumber(self.gf, other)
        if self.gf != other.gf:
            raise TypeError('Field sizes do not match')
        return ModularNumber(self.gf, self.value * other.value)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, int):
            return self / ModularNumber(self.gf, other)
        if self.gf != other.gf:
            raise TypeError('Field sizes do not match')
        # Find the inverse of other, then multiply that by self
        return self * ModularNumber.inverse(other)

    @staticmethod
    def inverse(num):
        ''' Find multiplicative inverse. Raise ValueError if none exists. '''
        t = 0
        new_t = 1
        r = num.gf.size
        new_r = num.value
        while new_r != 0:
            quotient = r // new_r
            (t, new_t) = (new_t, t - quotient * new_t)
            (r, new_r) = (new_r, r - quotient * new_r)
        if r > 1:
            raise ValueError('No inverse for {} mod {}'.format(num.value, num.gf.size))
        if t < 0:
            t += num.gf.size
        return ModularNumber(num.gf, t)


class GF():
    def __init__(self, size):
        self.size = size

    def __eq__(self, other):
        return self.size == other.size

    def __call__(self, x):
        return ModularNumber(self, x)
