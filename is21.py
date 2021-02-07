import click
from modules.levenshtein import calc_distance
from modules.dice import calc_dice
from modules.markov import calc_hmm, detect_words
import modules.art as art


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


@cli.command()
@click.option('--file', '-f', required=True, type=str, help='Define typed data file location')
@click.option('--transitions/--no-tran', '-t', default=False, type=bool, help='Show founded transitions')
@click.option('--emissions/--no-emis', '-e', default=False, type=bool, help='Show founded emission')
@click.option('--data/--no-data', '-d', default=False, type=bool, help='Show input data')
@click.option('--sentence', '-s', default="", type=str, help='Detects labels in given string')
def hmm(file, transitions, emissions, data, sentence):
    """Creates Markov model for given data"""
    art.print_hmm()
    calc_hmm(file, transitions, emissions, data, sentence)



if __name__ == '__main__':
    cli()
