import click
from levenshtein import distance
import art


@click.group()
def cli():
    pass


@cli.command()
@click.option('--words', '-w', type=click.Tuple([str, str]), default=[None, None], help='Defines two words to calculate')
@click.option('--table/--no-table', '-t', default=False, help='Show full table of values', )
def lev(words, table):
    """Calculates Levenshtein distance between first and second WORDs """
    art.print_lev()
    if all(words):
        (first, second) = words
    else:
        first: str = click.prompt('Enter first word', type=str)
        second: str = click.prompt('Enter second word', type=str)
        table: bool = click.confirm('Display table?')
    click.echo('Calculating Levenshtein distance')
    distance(first, second, table)


@cli.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello2(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


if __name__ == '__main__':
    cli()
