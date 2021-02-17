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


def print_matrix(a, b, d, m, n):
    matrix = []
    for s in b:
        matrix.append([""] * len(a) + [""] + list(s))
    for i in range(m + 1):
        row = []
        if i == 0:
            row += [""] * len(a)
        else:
            row += get(a, i - 1)
        for j in range(n + 1):
            row.append(d[(i, j)])
        matrix.append(row)
    print("\nAlignment of " + ", ".join(a) + " with " + ", ".join(b))
    print(tabulate(matrix))


def gap(a):
    """Returns n gaps for an alignment of n sequences."""
    return ["-"] * len(a)


def cmp(a, b):
    """Returns the score for comparing a and b, which may be characters or the gap symbol.
    cmp defines the scoring scheme for the string distance."""
    if a == "-" or b == "-":
        return 1
    else:
        return int(a != b)


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

    def align(self, a, b, d_dir, i, j):
        """Outputs the alignment of alignments a and b up to position i and j given the direction matrix d_dir.
        Alignments a and b are lists of strings with the original character sequences possibly with gaps."""
        if i == 0 and j == 0:
            return [[""] * len(a), [""] * len(b)]
        elif d_dir[i, j] == "W":
            (a2, b2) = self.align(a, b, d_dir, i, j - 1)
            return [add(a2, gap(a)), add(b2, get(b, j - 1))]
        elif d_dir[i, j] == "N":
            (a2, b2) = self.align(a, b, d_dir, i - 1, j)
            return [add(a2, get(a, i - 1)), add(b2, gap(b))]
        elif d_dir[i, j] == "NW":
            (a2, b2) = self.align(a, b, d_dir, i - 1, j - 1)
            return [add(a2, get(a, i - 1)), add(b2, get(b, j - 1))]

    def lev(self, a, b):
        """Align the two alignments a and b and return the common alignment and its score."""
        m = len(a[0])
        n = len(b[0])
        d = dict()
        d_dir = dict()
        d[(0, 0)] = 0
        d_dir[(0, 0)] = ""
        for i in range(1, m + 1):
            d[(i, 0)] = i * len(a) * len(b)
            d_dir[(i, 0)] = "N"
        for j in range(1, n + 1):
            d[(0, j)] = j * len(a) * len(b)
            d_dir[(0, j)] = "W"
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                (d[(i, j)], d_dir[(i, j)]) = min_dir(
                    d[(i - 1, j)] + sum_of_pairs(get(a, i - 1), gap(b)),
                    d[(i, j - 1)] + sum_of_pairs(gap(a), get(b, j - 1)),
                    d[(i - 1, j - 1)] + sum_of_pairs(get(a, i - 1), get(b, j - 1)))
        if self.verbose == 3:
            print_matrix(a, b, d, m, n)
        (a1, a2) = self.align(a, b, d_dir, m, n)
        a1.extend(a2)
        return d, a1

    def msa(self):
        """Progressive multiply alignment of the sequences in a.

        Successively, the sequences in a are added to an alignment.
        The final alignment and the sum of the scores are returned."""
        b = [self.words[0]]
        d = dict()
        c = []
        total = 0
        old_len = 0
        for i in range(1, len(self.words)):
            c = [self.words[i]]
            (d, b) = self.lev(b, c)
            score = d[(len(b[0]), len(c[0]))]
            total += score
            # increase the total score if previous alignment was shorter and gaps were inserted
            if i != 1 and old_len < len(b[1]):
                total += (len(b) - 1) * (len(b) - 2) / 2
            old_len = len(b[1])

        if self.verbose == 2:
            print_matrix(b, c, d, len(b[0]), len(c[0]))

        if len(self.words) > 2:
            print("\nAlignment:")
            for mm in b:
                print(mm)

        return total, b


def calc_distance(words, verbose=0):
    print("\nMultiply sequence alignment")

    cleaned = [word for word in words if word]
    levenshtein = Levenshtein(cleaned, verbose)

    score, _ = levenshtein.msa()

    print("\nTotal score: %d \n" % score)
