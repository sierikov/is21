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
    """Returns the list of characters at position i in the alignment a, which is a list of strings."""
    return list(map(lambda s: s[i], a))


def add(a, aas):
    """Given a list of n strings (an alignment) and a list of n characters, add appends character i to string i."""
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
    """Returns n gaps for an alignment of n sequences."""
    return ["-"] * len(a)


def cmp(word_1, word_2):
    """Returns the score for comparing a and b, which may be characters or the gap symbol.
    cmp defines the scoring scheme for the string distance."""
    if word_1 == "-" or word_2 == "-":
        return 1
    else:
        return int(word_1 != word_2)


def sum_of_pairs(aa, bb):
    """Computes the sum of pairs of all characters in string Word1 against all characters in string bb.
    aa and bb are alignments and may contain the gap symbol."""
    c = 0
    for a in aa:
        for b in bb:
            c += cmp(a, b)
    return c


class Levenshtein:

    def __init__(self, words, verbose):
        self.words = words
        self.verbose = verbose + 1

    def align(self, word_1, word_2, d_dir, i, j):
        """Outputs the alignment of alignments a and b up to position i and j given the direction matrix d_dir.
        Alignments a and b are lists of strings with the original character sequences possibly with gaps."""
        if i == 0 and j == 0:
            return [[""] * len(word_1), [""] * len(word_2)]
        elif d_dir[i, j] == "W":
            (a2, b2) = self.align(word_1, word_2, d_dir, i, j - 1)
            return [add(a2, gap(word_1)), add(b2, get(word_2, j - 1))]
        elif d_dir[i, j] == "N":
            (a2, b2) = self.align(word_1, word_2, d_dir, i - 1, j)
            return [add(a2, get(word_1, i - 1)), add(b2, gap(word_2))]
        elif d_dir[i, j] == "NW":
            (a2, b2) = self.align(word_1, word_2, d_dir, i - 1, j - 1)
            return [add(a2, get(word_1, i - 1)), add(b2, get(word_2, j - 1))]

    def lev(self, word_1, word_2):
        """Align the two alignments a and b and return the common alignment and its score."""
        word_1_length = len(word_1[0])
        word_2_length = len(word_2[0])
        values_dic = dict()
        d_dir = dict()
        values_dic[(0, 0)] = 0
        d_dir[(0, 0)] = ""
        for i in range(1, word_1_length + 1):
            values_dic[(i, 0)] = i * len(word_1) * len(word_2) + int(i * len(word_2) * (len(word_2) - 1) / 2)
            d_dir[(i, 0)] = "N"
        for j in range(1, word_2_length + 1):
            values_dic[(0, j)] = j * len(word_1) * len(word_2) + int(j * len(word_1) * (len(word_1) - 1) / 2)
            d_dir[(0, j)] = "W"
        for i in range(1, word_1_length + 1):
            for j in range(1, word_2_length + 1):
                (values_dic[(i, j)], d_dir[(i, j)]) = min_dir(
                    values_dic[(i - 1, j)] + sum_of_pairs(get(word_1, i - 1), gap(word_2)) + int(len(word_2) * (len(word_2) - 1) / 2),
                    values_dic[(i, j - 1)] + sum_of_pairs(gap(word_1), get(word_2, j - 1)) + int(len(word_1) * (len(word_1) - 1) / 2),
                    values_dic[(i - 1, j - 1)] + sum_of_pairs(get(word_1, i - 1), get(word_2, j - 1))
                )
        if self.verbose == 2:
            print_matrix(word_1, word_2, values_dic)
        (a1, a2) = self.align(word_1, word_2, d_dir, word_1_length, word_2_length)
        a1.extend(a2)
        return (a1, values_dic[(word_1_length, word_2_length)])

    def msa(self):
        """Progressive multiply alignment of the sequences in a.

        Successively, the sequences in a are added to an alignment.
        The final alignment and the sum of the scores are returned."""
        word_1 = [self.words[0]]
        total = 0
        for i in range(1, len(self.words)):
            word_2 = [self.words[i]]
            (word_1, score) = self.lev(word_1, word_2)
            total += score

        if len(self.words) > 2:
            print("\nAlignment:")
            for mm in word_1:
                print(mm)

        return total, word_1


def calc_distance(words, verbose=0):
    print("\nMultiply sequence alignment")

    cleaned = [word for word in words if word]
    levenshtein = Levenshtein(cleaned, verbose)

    score, _ = levenshtein.msa()

    print("\nTotal score: %d \n" % score)
