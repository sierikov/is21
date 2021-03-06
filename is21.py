import click
from modules.arg import calc_arg
from modules.lev import calc_lev
from modules.dice import calc_dice
from modules.markov import calc_hmm
import modules.art as art


def get_words(initial):
    if all(initial):
        return initial
    else:
        first: str = click.prompt('Enter first word', type=str)
        second: str = click.prompt('Enter second word', type=str)
    return first, second


@click.group()
def cli():
    pass


@cli.command()
@click.option('--words', '-w', multiple=True, required=True, help='Defines words to calculate distance')
@click.option('--optimum/--greedy', '-o', default=False, type=bool, help='Will use A* to optimize search')
@click.option('--verbose', '-v', count=True, help='Defines log level of output')
def lev(words, optimum, verbose):
    """Calculates Levenshtein distance between first and second WORDs """
    art.print_lev()
    words = get_words(words)
    calc_lev(words, optimum, verbose)


@cli.command()
@click.option('--words', '-w', type=click.Tuple([str, str]), required=True,
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
@click.option('--start', default="$", type=str, help="Indicates the start of the sentence")
@click.option('--end', default="#", type=str, help="Indicetes the end of the sentence")
def hmm(file, transitions, emissions, data, sentence, start, end):

    """Creates Markov model for given data"""
    art.print_hmm()
    calc_hmm(file, transitions, emissions, data, sentence, start, end)


@cli.command()
@click.option('--file', '-f', required=True, type=str, help='Define typed data file location')
@click.option('--data/--no-sd', '-sd', default=False, type=bool, help='Show input data')
@click.option('--rebut/--no-r', '-re', default=False, type=bool, help='Show all rebuts')
@click.option('--attack/--no-a', '-at', default=False, type=bool, help='Show all attacks')
@click.option('--defeat/--no-d', '-de', default=False, type=bool, help='Show all defeats')
@click.option('--undercut/--no-u', '-un', default=False, type=bool, help='Show all undercuts')
@click.option('--s-attack/--no-sa', '-sa', default=False, type=bool, help='Show all strong attacks')
@click.option('--s-undercut/--no-su', '-su', default=False, type=bool, help='Show all strong undercuts')
@click.option('--all/--some', '-a', default=False, type=bool, help='Show all types that can be found')
def arg(file, data, rebut, attack, defeat, undercut, s_attack, s_undercut, all):

    """Checks if given arguments contains rebuts, attacks or defeats"""
    art.print_arg()
    calc_arg(file, data, rebut, attack, defeat, undercut, s_attack, s_undercut, all)


if __name__ == '__main__':
    cli()
