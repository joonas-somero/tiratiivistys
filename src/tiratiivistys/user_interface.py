from typing import BinaryIO

import click

from tiratiivistys import huffman, lempel_ziv
from tiratiivistys.compressor import Compressor


@click.command()
@click.option("--compress/--restore", "-c/-r",
              required=True,
              help="operation")
@click.option("--algorithm", "-a",
              required=True,
              type=click.Choice(choices=("Huffman", "LZW"),
                                case_sensitive=False),
              help="compression algorithm (case insensitive)")
@click.argument("input_file", type=click.File("rb"))
@click.argument("output_file", type=click.File("wb"))
def command_line_interface(compress: bool,
                           algorithm: str,
                           input_file: click.File,
                           output_file: click.File) -> None:
    """Compress or restore INPUT_FILE into OUTPUT_FILE,
    overwriting existing OUTPUT_FILE.
    """

    module = {"Huffman": huffman,
              "LZW": lempel_ziv}[algorithm]
    model = (module.Encoder
             if compress
             else module.Decoder)

    if model is not None:
        click.echo(click.style(("Compressing"
                                if compress
                                else "Restoring"), fg="bright_white")
                   + " "
                   + click.style(input_file.name, fg="cyan")
                   + " into "
                   + click.style(output_file.name, fg="yellow")
                   + " using "
                   + click.style(algorithm, fg="bright_white")
                   + "...")

        compressor = Compressor(model, input_file, output_file)
        compressor.deploy()

        click.echo("Finished.")
