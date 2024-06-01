from urllib import request
from tempfile import TemporaryFile, NamedTemporaryFile
from math import ceil
from itertools import batched

from tiratiivistys.constants import N_BITS


def get_named_file(content):
    fp = NamedTemporaryFile()
    fp.write(content)
    fp.seek(0)
    return fp


def get_remote_file(url):
    with request.urlopen(url) as f:
        return get_named_file(f.read())


def get_empty_file():
    return TemporaryFile()


def codeword_to_bytes(codeword):
    def binary_string(integer):
        return format(integer, 'b').rjust(N_BITS, '0')

    def padded(bin_str):
        n_bytes = ceil((2*N_BITS) / 8)
        return bin_str.ljust(8*n_bytes, '0')

    binary = padded(binary_string(codeword.offset) +
                    binary_string(codeword.length))

    return bytes([int(''.join(byte), 2)
                  for byte
                  in list(batched(binary, 8))])
