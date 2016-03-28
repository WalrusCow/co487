from ecc import EllipticCurve
from field import GF

class Checker():
    prime = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    curve = EllipticCurve(0, 7, GF(prime))

    G = curve.pt(
            0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
            0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
    # q is the order of G
    q = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    field = GF(q)

    P = curve.pt(
            0xbac380aaefa5c656280bea4093ce7a06677f37c43bd121d5720b9ed2a6e1e2a5,
            0x5d88d4b08d21963b9a5c47ca9f875b05cb42237444727d5b42eb17a0f8d9dc40)
    hash = field(0xc0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a)
    r = field(0x32d80046e3257c4fe9b948e9b5b4d4aa4fcf05dff9bad6e056528f622f626b8c)
    s = field(0x10e669184888d1427e0e3f0fd4d345cc7cec53f7be0688e58a7d858f3471c995)

    @staticmethod
    def check_key(key):
        calc_r = (key * Checker.G).x
        if Checker.r.value != calc_r.value:
            return False
        # Probably right!
        sekrit_key = (Checker.s * key - Checker.hash) / Checker.r
        print('Found sekrit key: {}'.format(sekrit_key))
        key_valid = (sekrit_key.value * Checker.G) == Checker.P
        print('sekrit * G == P? {}'.format(key_valid))
        return sekrit_key if key_valid else None


def get_possible_bits(side_data):
    left_bit_list = [['0']]
    right_bit_list = [['0']]
    bit_list = left_bit_list
    for c in side_data:
        if c == 'A':
            bit_list[-1] = ['1']
        elif c == 'D':
            bit_list.append(['0'])
        elif c == '*':
            # Either add a 0 or change the last one to a 1.
            bit_list[-1] = ['1', '00']
        elif c == '.':
            # just add to the known bits on the right, then
            bit_list = right_bit_list
    left_bit_list.pop()
    right_bit_list = right_bit_list[1:]
    return left_bit_list, right_bit_list


def possible_strings(list_of_options):
    base_string = ''
    possibilities = []
    for s in list_of_options:
        if len(s) == 1:
            base_string += s[0]
        else:
            base_string += '{}'
            possibilities.append(s)

    def _possible_strings(list_of_options, acc):
        if not list_of_options:
            yield base_string.format(*acc)
            return
        for option in list_of_options[0]:
            yield from _possible_strings(list_of_options[1:], acc + [option])

    return _possible_strings(possibilities, [])


def all_bits(l):
    ''' Generator for all binary strings of length l. '''
    def _genner(n, acc):
        if n <= 0:
            yield acc
            return
        for b in ('0', '1'):
            yield from _genner(n - 1, acc + b)
    return _genner(l, '')


def check_keys(left_bits, right_bits, mid_len):
    for mid_bits in all_bits(mid_len):
        possible_key = left_bits + mid_bits + right_bits
        if Checker.check_key(int(possible_key, 2)):
            return possible_key
    return None


def find_key(side_data):
    left_bits, right_bits = get_possible_bits(side_data)
    for lbs in possible_strings(left_bits):
        for rbs in possible_strings(right_bits):
            # The key could be up to 256 bits, but we will assume *exactly*
            max_mid_len = 256 - (len(lbs) + len(rbs))
            result = check_keys(lbs, rbs, max_mid_len)
            if result is not None:
                return result

if __name__ == '__main__':
    import sys
    # Silly Python...
    sys.setrecursionlimit(2000)

    with open('side_data.txt') as f:
        side_data = f.read().strip()
    print(find_key(side_data))
