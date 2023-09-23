import click
from .huffman import Huffman
from .lempel_ziv import LempelZiv


@click.command()
@click.option('--algorithm', '-a',
              required=True,
              type=click.Choice(choices=('Huffman', 'Lempel-Ziv'),
                                case_sensitive=False),
              help='compression algorithm to use')
@click.option('--compress', '-c',
              is_flag=True,
              help='compress FILE')
@click.argument('file', type=click.File('rb'))
def command_line_interface(compress, algorithm, file):
    """Restore previously compressed FILE to original, or compress FILE."""

    verb = compress and 'Compressing' or 'Restoring'
    click.echo(
        f"{verb} {file.name} using {algorithm}...")

    selected = algorithm.lower()
    operation = compress and "compress" or "restore"
    imports = {"huffman": Huffman, "lempel-ziv": LempelZiv}

    getattr(imports[selected], operation)(file)
