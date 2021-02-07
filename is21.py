import click
from levenshtein import calc_distance
from dice import calc_dice
import art


def get_words(initial):
    if all(initial):
        (first, second) = initial
    else:
        first: str = click.prompt('Enter first word', type=str)
        second: str = click.prompt('Enter second word', type=str)
    return first, second


@click.group()
def cli():
    pass


@cli.command()
@click.option('--words', '-w', type=click.Tuple([str, str]), default=[None, None],
              help='Defines two words to calculate')
@click.option('--table/--no-table', '-t', default=False, help='Show full table of values', )
def lev(words, table):
    """Calculates Levenshtein distance between first and second WORDs """
    art.print_lev()
    (first, second) = get_words(words)
    click.echo('Calculating Levenshtein distance')
    calc_distance(first, second, table)


@cli.command()
@click.option('--words', '-w', type=click.Tuple([str, str]), default=[None, None],
              help='Defines two words to calculate')
@click.option('--trigrams/--no-trigrams', '-t', default=False, help='Show trigrams for each word', )
def dice(words, trigrams):
    """Calculates Dice coefficient for given WORDs"""
    art.print_dice()
    (first, second) = get_words(words)
    calc_dice(first, second, trigrams)


if __name__ == '__main__':
    cli()
