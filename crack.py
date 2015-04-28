__author__ = 'ricardo.moreira@acad.pucrs.br'

import sys
import argparse
import base64
import itertools


def hex2string(buff):
    output = base64.b16decode(buff)
    return output


def xor(a):
    return chr(ord(a[0]) ^ ord(a[1]))


def encode(data, pad):
    encoded = ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(data, pad)])
    return encoded


def main(argv):
    description = "One-Time Pad Breaker"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', metavar='in-file', type=argparse.FileType('rt'), help='the file to process',
                        required=True)
    args = parser.parse_args()

    # get all ciphertext
    ciphers = [a.strip().upper() for a in args.i.readlines()]
    #print 'ciphers:', ciphers

    c1 = list(hex2string(ciphers[0]))
    c2 = list(hex2string(ciphers[1]))
    x = map(xor, zip(c1, c2))

    print '       C1:', c1
    print '       C2:', c2
    print 'C1 xor C2:', x

    x = map(xor, zip(c1, itertools.repeat(' ')))
    print 'C1 xir sp:', x

if __name__ == "__main__":
    main(sys.argv[1:])

