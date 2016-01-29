from functools import reduce

def to_bin(n, digits=4): return bin(n)[2:].rjust(digits, '0')
def from_bin(s): return int(s, 2)

class SBox():
    sub_mat = {
        0: 14, 1: 4, 2: 13, 3: 1,
        4: 2, 5: 15, 6: 11, 7: 8,
        8: 3, 9: 10, 10: 6, 11: 12,
        12: 5, 13: 9, 14: 0, 15: 7,
    }
    inv_mat = {}
    for k, v in sub_mat.items():
        inv_mat[v] = k

    @classmethod
    def apply(cls, n):
        return to_bin(cls.sub_mat[from_bin(n)], 4)

    @classmethod
    def invert(cls, n):
        return to_bin(cls.inv_mat[from_bin(n)], 4)


def xor(a, b):
    ''' xor two bit strings. '''
    assert len(a) == len(b)
    assert all(c in '01' for c in a)
    assert all(c in '01' for c in b)
    def xor_char(c1, c2):
        return str(int(a != b))
    return ''.join(xor_char(c1, c2) for c1, c2 in zip(a, b))


def relation_input(U, P):
    return (U[5], U[7], U[13], U[15], P[4], P[6], P[7])


def find_the_bias(plaintexts, ciphertexts, partial_key):
    assert len(partial_key) == 2
    k58_guess = partial_key[0]
    k516_guess = partial_key[1]

    relation_holds_count = 0
    total = 0
    for P, C in zip(plaintexts, ciphertexts):
        total += 1
        c58 = C[4:8]
        v58 = xor(c58, k58_guess)
        u58 = SBox.invert(v58)

        v516 = xor(C[12:16], k516_guess)
        u516 = SBox.invert(v516)

        U = '????' + u58 + '????' + u516

        relation_holds = reduce(xor, relation_input(U, P)) == '0'
        if relation_holds:
            relation_holds_count += 1
    return abs(0.5 - (relation_holds_count / total))


def find_best_key(plaintexts, ciphertexts):
    max_bias = 0
    for k8 in range(2**4):
        for k16 in range(2**4):
            key_guess = (to_bin(k8), to_bin(k16))
            bias = find_the_bias(plaintexts, ciphertexts, key_guess)
            if bias > max_bias:
                max_bias = bias
                best_key_guess = key_guess
    return best_key_guess


def main():
    with open('l_plain.txt') as pf, open('l_ciphers.txt') as cf:
        plaintexts = list(map(str.strip, pf))
        ciphertexts = list(map(str.strip, cf))
    bias = find_the_bias(plaintexts, ciphertexts, ('0111', '0110'))
    print('Question 2a: The bias is {}'.format(str(bias)))
    best_key = find_best_key(plaintexts, ciphertexts)
    print('Question 2b: The best key guess is {}'.format(best_key))


if __name__ == '__main__':
    main()
