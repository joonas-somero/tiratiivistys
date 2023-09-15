import click


@click.command()
@click.option('--compress', '-c',
              is_flag=True,
              help='compress FILE')
@click.argument('file', type=click.File('rb'))
def command_line_interface(compress, file):
    """Restore previously compressed FILE to original, or compress FILE."""
    operation = compress and "Compressing" or "Restoring"
    click.echo(f"{operation} {file.name}...")
