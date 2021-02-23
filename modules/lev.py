from modules.levenshtein.astar import LevenshteinA
from modules.levenshtein.greedy import LevenshteinG


def calc_lev(words, optimum=False, verbose=0):
    print("\nMultiply sequence alignment")

    cleaned = [word for word in words if word]
    if optimum:
        levenshtein = LevenshteinA(cleaned, verbose)
    else:
        levenshtein = LevenshteinG(cleaned, verbose)

    score, _ = levenshtein.msa()

    print("\nTotal score: %d \n" % score)