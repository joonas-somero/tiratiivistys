from tests.helpers import get_remote_file, get_empty_file
from tiratiivistys import huffman, lempel_ziv
from tiratiivistys.compressor import Compressor


SUMMARY_FILENAME = "summary.md"

PROTOCOL = "https"
SITE = "www.gutenberg.org"
PATH = "ebooks"
FORMAT = ".txt.utf-8"

BOOKS = [{"name": "Alice's Adventures in Wonderland", "id": "28885"},
         {"name": "Kalevala", "id": "5186"},
         {"name": "War and Peace", "id": "2600"}]

SUPPLEMENTAL = [{"name": "Green Eggs and Ham",
                 "url": "https://cse.sc.edu/~rose/587/greeneggsandham.txt"}]

MATERIAL = []

ALGORITHMS = [{"name": "Huffman", "encoder": huffman.Encoder},
              {"name": "Lempel-Ziv", "encoder": lempel_ziv.Encoder}]


def get_book_file(book):
    print(f"Fetching '{book['name']}' from {SITE}...")
    url = f"{PROTOCOL}://{SITE}/{PATH}/{book['id']}{FORMAT}"
    return get_remote_file(url)


def file_size(file_object):
    file_object.seek(0, 2)
    size = file_object.tell()
    file_object.seek(0)
    return size


def compress_with(algorithm, input_file):
    output_file = get_empty_file()
    compressor = Compressor(algorithm['encoder'],
                            input_file,
                            output_file)
    compressor.deploy()
    input_file.seek(0)
    return output_file


def compare_file_sizes(item, algorithm):
    print(f"Compressing '{item['name']}' using {algorithm['name']}...")
    input_file = item["file"]
    output_file = compress_with(algorithm, input_file)
    return item["size"], file_size(output_file)


def get_file_size(size):
    return "{:.2f}".format(size / 1024)


def get_compression_ratio(original_size, compressed_size):
    return "{:.2f}".format(original_size / compressed_size)


def get_values(algorithm):
    return [get_compression_ratio(*result)
            for result in [compare_file_sizes(book, algorithm)
                           for book in MATERIAL]]


def get_table_row(values):
    return " | ".join(values)


def get_row(algorithm):
    values = get_values(algorithm)
    name = algorithm["name"]
    return get_table_row([name] + values)


def get_table(columns, rows):
    return [
        get_table_row(columns),
        get_table_row(["---"] * len(columns))
    ] + rows


def get_section(level, heading, rows):
    section = (rows
               if all(isinstance(row, str) for row in rows)
               else [row for subsection in rows for row in subsection])
    return [
        "#" * level + " " + heading,
        ""
    ] + section + [""]


def write_summary(filename):
    size_columns = ["File", "KiB"]
    size_rows = [get_table_row([item["name"], get_file_size(item["size"])])
                 for item in MATERIAL]
    size_table = get_table(size_columns, size_rows)

    ratio_columns = ["-"] + [item["name"] for item in MATERIAL]
    ratio_rows = [get_row(algorithm) for algorithm in ALGORITHMS]
    ratio_table = get_table(ratio_columns, ratio_rows)

    sections = get_section(1, "Summary", [
        get_section(2, "File sizes", size_table),
        get_section(2, "Compression ratios", ratio_table)
    ])

    with open(filename, "wt") as fp:
        print(f"Writing summary into '{SUMMARY_FILENAME}'...")
        fp.writelines([line + "\n" for line in sections])


def init_material():
    def size(f): return file_size(f)

    def include_books():
        for book in BOOKS:
            book_file = get_book_file(book)
            book["file"] = book_file
            book["size"] = size(book_file)
            MATERIAL.append(book)

    def include_supplemental():
        for item in SUPPLEMENTAL:
            url = item["url"]
            print("Fetching supplemental material...")
            item_file = get_remote_file(url)
            item["file"] = item_file
            item["size"] = size(item_file)
            MATERIAL.append(item)

    include_books()
    include_supplemental()

    def size_key(item): return item["size"]
    MATERIAL.sort(key=size_key)


if __name__ == "__main__":
    init_material()
    write_summary(SUMMARY_FILENAME)
