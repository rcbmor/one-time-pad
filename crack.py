__author__ = 'ricardo.moreira@acad.pucrs.br'

import sys
import base64
import itertools
import collections


def hex2string(buff):
    output = base64.b16decode(buff.upper())
    return output


def xor(a, b):
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def encode(data, pad):
    encoded = ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(data, pad)])
    return encoded


def set_at(counters, i, j, k, v):
    counters[i][k][v] += 1
    counters[i][k][' '] += 1
    counters[j][k][v] += 1
    counters[j][k][' '] += 1


def init_counters(ciphers):
    counters = []
    m = len(ciphers)
    for i in range(0, m):
        cipher_counters = []
        for j in range(0, len(ciphers[i])):
            cipher_counters.append(collections.Counter())
        counters.append(cipher_counters)
    return counters


def populate_counters(ciphers, counters):
    m = len(ciphers)
    for i in range(0, m):
        for j in range(i + 1, m):
            x = xor(ciphers[i], ciphers[j])
            print 'XOR', i, j, ':', list(x)
            # count prob of letter.swapcase or space
            for k in range(0, len(x)):
                v = x[k]
                if v.isalpha():
                    # c_i xor c_j = v , v = V or ' '
                    _v = v.swapcase()
                    set_at(counters, i, j, k, _v)
    return counters


def find_plain_texts(counters):
    plain_texts = []
    i = 0
    for ci in counters:
        j = 0
        plain = []
        for c in ci:
            if len(c) == 0:  # could not find
                plain.append('?')
                continue
            elif len(c) == 2:
                c.pop(' ')  # assume is the other letter
                p = c.keys()[0]
                plain.append(p)
                continue
            # calculate
            s = sum(c.values())
            probs = map(lambda a: (a[0], float(a[1])/s), c.items())
            it = reduce(lambda a, b: a if a[1] > b[1] else b, probs)
            plain.append(it[0])

            j += 1
        plain_texts.append(plain)
        i += 1
    return plain_texts


def find_key(ciphers, planis):
    key = None
    return key


def main(argv):
    cipher_texts = [
        "3939252352554c5f51592621294d5c5229382f5d454b485d4554413132275458482d3157415046495c5b2a435a46543527364d5059394847382a2b4b555746404a38202d4c525652455c2a",
        "4d514c503134405f305f4e44292c41534a57414f2c2c2d4054544d5f552741424c5931345f415d2c2e4d4454405e504142522e31424a434c5f2a2b415a412f585a55452d2e20394941562a",
        "56574023455d4449305b4745295b5b5a45385f59435a44574526453132445c5a454843404d585a2c4146464e3246544146554531445c49574a435f573a",
        "505725575951292c53594f515d435544484847522c2c4e5f4155575441274c45582d465d444c2e404b495859324f4f4227424131545644444d594e2e554a4b2c4757204947465f4c53572a",
        "4d5625565f504c5e435f474f4d2c565f5a5b5d4e58492d4352494650504e59435954315d5b2047415e4758435349543553592e44595d4f504b5e4a4050244c5e4a48544249525849484b2a",
        "5c57424f5847412c5c4e52554c5e41364f4a4a5a594943505926455d5e4842592d545e412854412c4c5a4f565927565c40534054455c2a43564e2b4d55415c4d413843445e485c4b533c",
        "5a4b5c53455b4e5e515b4e5829454136594a4a584942593349482442575150584c413150414648495c4d44433253594542452e5e51394b524846424d555046435d4b20434157585d414b5722",
        "505f255a5e41294a5f5e484529585a532957414e2c58445e45265450562b355e45485f34514f5b2c46495c523241495b4e45465453395e4a51592b2e574b5a5e405d57425c4b37",
        "5c6f607168346a607f7e6221616d613668387c62607a6861206a6d7f7b697224"
    ]

    ciphers = map(hex2string, cipher_texts)
    for i in range(len(ciphers)):
        print 'C', i, ':', ciphers[i]

    #c1 = list(hex2string(cipher_texts[0]))
    #c2 = list(hex2string(cipher_texts[1]))
    #x = (c1, c2)
    #print '       C1:', c1
    #print '       C2:', c2
    #print 'C1 xor C2:', x

    # matrix of counters for probabilities
    counters = init_counters(ciphers)

    # permute xor on ciphers
    populate_counters(ciphers, counters)

    plain_texts = find_plain_texts(counters)
    for i in range(len(plain_texts)):
        print 'P', i, ':', "".join(plain_texts[i])

    key = find_key(ciphers, plain_texts)
    print 'Key:', key

if __name__ == "__main__":
    main(sys.argv[1:])

