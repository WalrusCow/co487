import string
letter_map = ' ' + string.ascii_letters[26:]

def to_number(char):
    """ Convert a character to a number for use in adding stuff. """
    try:
        return letter_map.index(char)
    except ValueError as e:
        raise ValueError('Char "{}" is invalid'.format(char))

def to_letter(num):
    try:
        return letter_map[num]
    except IndexError as e:
        raise ValueError('Number {} is not valid'.format(str(num)))

def add(a, b):
    return (a + b) % 27

def sub(a, b):
    return (a - b) % 27

def encrypt(str, key):
    if len(str) != len(key):
        raise ValueError('String and key must be of equal length')
    str_nums = (to_number(c) for c in str)
    key_nums = (to_number(c) for c in key)
    return ''.join(to_letter(add(s, k)) for s, k in zip(str_nums, key_nums))

def decrypt(str, key):
    if len(str) != len(key):
        raise ValueError('String and key must be of equal length')
    str_nums = (to_number(c) for c in str)
    key_nums = (to_number(c) for c in key)
    return ''.join(to_letter(sub(s, k)) for s, k in zip(str_nums, key_nums))
