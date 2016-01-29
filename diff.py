from operator import itemgetter

SBOX_SIZE = 4

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
        return to_bin(cls.sub_mat[from_bin(n)])

    @classmethod
    def invert(cls, n):
        return to_bin(cls.inv_mat[from_bin(n)])


def xor(a, b):
    ''' xor two bit strings. '''
    assert len(a) == len(b)
    assert all(c in '01' for c in a)
    assert all(c in '01' for c in b)
    def xor_char(c1, c2):
        return str(int(c1 != c2))
    return ''.join(xor_char(c1, c2) for c1, c2 in zip(a, b))


def format_key(key, bit_guesses):
    out = ''
    guess_idx = 0
    for c in key:
        if c == '?':
            out += bit_guesses[guess_idx]
            guess_idx += 1
        else:
            out += c
    return out


def get_s_box_bits(text, s_box):
    ''' Get the bits corresponding to an s-box index. '''
    return text[SBOX_SIZE * s_box:SBOX_SIZE * (s_box + 1)]


def prune_texts(plaintexts, ciphertexts, key):
    s_boxes = []
    for s_box in range(0, 4):
        key_bits = get_s_box_bits(key, s_box)
        if any(c not in '01?' for c in key_bits):
            s_boxes.append(s_box)

    valid_plaintexts = []
    valid_ciphertexts = []
    for ((p1, p2), (c1, c2)) in zip(plaintexts, ciphertexts):
        cx = xor(c1, c2)
        # All these s boxes are all 0
        if all('1' not in get_s_box_bits(cx, sb) for sb in s_boxes):
            valid_plaintexts.append((p1, p2))
            valid_ciphertexts.append((c1, c2))
    return valid_plaintexts, valid_ciphertexts



def count_matching(plaintexts, ciphertexts, delta_u, key):
    ''' Count the number of pairs that match delta u. '''
    def s_box_matches(c1, c2, s_box):
        # Extract bits for our s box
        key_bits = get_s_box_bits(key, s_box)
        if 'x' in key_bits:
            # We have already pruned these out.
            return True
        delta_u_bits = get_s_box_bits(delta_u, s_box)
        v1_bits = xor(get_s_box_bits(c1, s_box), key_bits)
        v2_bits = xor(get_s_box_bits(c2, s_box), key_bits)
        return delta_u_bits == xor(SBox.invert(v1_bits), SBox.invert(v2_bits))

    matches = 0
    for c1, c2 in ciphertexts:
        if all(s_box_matches(c1, c2, s_box) for s_box in range(4)):
            matches += 1
    return matches


def find_key(plaintexts, ciphertexts, delta_u, key):
    # Get which bits we are looking for
    unknown_bits = [i for i, c in enumerate(key) if c == '?']
    max_count = 0
    best_guess = None

    print('Finding key {}. {} ciphertexts.'.format(key, len(ciphertexts)))
    # Prune the possible ciphertexts to remove those that don't match
    # on key bits we are not guessing (perf optimization).
    plaintexts, ciphertexts = prune_texts(plaintexts, ciphertexts, key)
    print('After pruning: {} ciphertexts.'.format(len(ciphertexts)))

    guesses = []

    for n in range(2 ** len(unknown_bits)):
        bin_guess = to_bin(n, digits=len(unknown_bits))
        key_guess = format_key(key, bin_guess)
        count = count_matching(plaintexts, ciphertexts, delta_u, key_guess)
        guesses.append((key_guess, count))
        if count > max_count:
            max_count = count
            best_guess = key_guess

    guesses = sorted(guesses, key=itemgetter(1), reverse=True)
    print('Top 20 guesses:')
    print('\n'.join(map(str, guesses[:20])))
    return key_guess, max_count


def main():
    p_texts = []
    c_texts = []

    with open('d_data.txt') as f:
        for l in map(str.strip, f):
            x1, x2, y1, y2 = l.split(',')
            p_texts.append((x1, x2))
            c_texts.append((y1, y2))

    delta_x = '0000101100000000'
    delta_u = '0000011000000110'
    key, count = find_key(p_texts, c_texts, delta_u, 'xxxx????xxxx????')
    print('Found key {} with {} delta U matches'.format(key, count))


if __name__ == '__main__':
    main()
