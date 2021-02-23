from tabulate import tabulate


def min_dir(a, b, c):
    """Returns the minimum value of a, b, and c and which are minimal.

    c is encoded as NW, b as N and a as W.
    More than one can be the minimum.
    Preference is given to NW, then N, then W.
    This means that alignments with match/mismatch
    from end to front are preferred. If all alignments
    are needed, then the function has to return a set of directions
    instead of single direction."""
    if c == min(a, b, c):
        return c, "NW"
    if b == min(a, b, c):
        return b, "W"
    if a == min(a, b, c):
        return a, "N"


def get(a, i):
    """
    Returns the list of characters at position i in the alignment a, which is a list of strings.
    """
    return list(map(lambda s: s[i], a))


def add(a, aas):
    """
    Given a list of n strings (an alignment) and a list of n characters, add appends character i to string i.
    """
    a2 = []
    for i in range(len(a)):
        a2.append(a[i] + aas[i])
    return a2


def print_matrix(word_1, word_2, score_dic):
    matrix = []
    word_1_length = len(word_1[0])
    word_2_length = len(word_2[0])
    for s in word_2:
        matrix.append([""] * len(word_1) + [""] + list(s))
    for i in range(word_1_length + 1):
        row = []
        if i == 0:
            row += [""] * len(word_1)
        else:
            row += get(word_1, i - 1)
        for j in range(word_2_length + 1):
            row.append(score_dic[(i, j)])
        matrix.append(row)
    print("\nAlignment of " + ", ".join(word_1) + " with " + ", ".join(word_2))
    print(tabulate(matrix))


def gap(a):
    """
    Returns n gaps for an alignment of n sequences.
    """
    return ["-"] * len(a)


def cmp(word_1, word_2):
    """
    Returns the score for comparing a and b, which may be characters or the gap symbol.
    cmp defines the scoring scheme for the string distance.
    """
    if word_1 == "-" or word_2 == "-":
        return 1
    else:
        return int(word_1 != word_2)


def sum_of_pairs(aa, bb):
    """
    Computes the sum of pairs of all characters in string Word1 against all characters in string bb.
    aa and bb are alignments and may contain the gap symbol.
    """
    c = 0
    for a in aa:
        for b in bb:
            c += cmp(a, b)
    return c
