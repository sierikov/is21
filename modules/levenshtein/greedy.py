from modules.levenshtein.utils import gap, get, add, sum_of_pairs, min_dir, print_matrix


class LevenshteinG:

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
                    values_dic[(i - 1, j)] + sum_of_pairs(get(word_1, i - 1), gap(word_2)) + int(
                        len(word_2) * (len(word_2) - 1) / 2),
                    values_dic[(i, j - 1)] + sum_of_pairs(gap(word_1), get(word_2, j - 1)) + int(
                        len(word_1) * (len(word_1) - 1) / 2),
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
