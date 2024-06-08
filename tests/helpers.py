from urllib import request
from tempfile import TemporaryFile, NamedTemporaryFile
from math import ceil


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


def get_max_int(n_bits):
    return (2**n_bits) - 1


def get_min_n_bytes(n_bits):
    return ceil(n_bits / 8)


def get_ones_justified(n_ones):
    total_bits = get_min_n_bytes(n_ones) * 8
    return (n_ones * '1').ljust(total_bits, '0')


def get_padded_bytes(n_ones):
    bin_string = get_ones_justified(n_ones)
    byte_size_chunks = [bin_string[i:i+8]
                        for i
                        in range(0, len(bin_string), 8)]
    return bytes([int(chunk, 2) for chunk in byte_size_chunks])


def get_bytes(integer):
    return integer.to_bytes(get_min_n_bytes(integer))


def get_byte_range(start, stop):
    return (get_bytes(i)
            for i
            in range(start, stop))
