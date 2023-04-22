from random import randint
from hashlib import sha256

# https://drive.google.com/file/d/106HnVHW4nBKMmZmay_EQK3KiKB9FnkFE/view
def hashThis(a, b, c):
    hash = sha256()
    hash.update(str(a).encode())
    hash.update(str(b).encode())
    hash.update(str(c).encode())
    return int(hash.hexdigest(), 16)


def convert_message_to_int(M):
    return int(sha256(M.encode()).hexdigest(), 16)


def gen_public_sig(X, M):
    m = convert_message_to_int(M)
    x = convert_message_to_int(X)
    a = 2  # Genrator Function
    p = 2695139  # prime number
    y = pow(a, x, p)
    r = randint(1, p - 1)
    t1 = pow(m, x, p)
    t2 = pow(m, r, p)
    t3 = pow(a, r, p)
    c = hashThis(t1, t2, t3)
    s = (c * x) + r
    tup = (y, s, t1, t2, t3)
    return tup

# verify


def verify(t):

    y, s, t1, t2, t3 = t

    a = 2  # Genrator Function
    p = 2695139  # prime number

    c = hashThis(t1, t2, t3)

    if (pow(a, s, p) == (pow(y, c, p) * t3) % p):
        return True
    return False


# print(verify(gen_public_sig(123, 'hi')))
