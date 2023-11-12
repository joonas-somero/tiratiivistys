from urllib import request
from tempfile import TemporaryFile, NamedTemporaryFile


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
