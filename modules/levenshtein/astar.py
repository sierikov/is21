from modules.levenshtein.utils import cmp
from modules.levenshtein.node import Node
from tabulate import tabulate
from typing import List
import queue as Q
import itertools


def transitioncost(cc):
    # cc are the characters for the successor
    cost = 0
    for i in range(len(cc)):
        for j in range(i + 1, len(cc)):
            cost += cmp(cc[i], cc[j])
    return cost


def get_path(node: Node):
    """
    Given the endnode 'node' backtrace the path to the startnode and return it.
    """
    path = []

    # pred of startnode is set to None
    while node is not None:
        path.insert(0, node)
        node = node.pred
    return path


class LevenshteinA:

    def __init__(self, words, verbose):
        self.words = words
        self.verbose = verbose + 1
        start_node = Node(chars_column=[""] * len(words),
                          kk=[0] * len(words),
                          g=0,
                          h=self.underestimation(words),
                          pred=None)
        self.start_node = start_node
        # create a priority queue, the elements are ordered by the total cost f
        queue = Q.PriorityQueue()
        queue.put(start_node)
        self.queue = queue

    def append_neighbors(self, node: Node):
        # get next characters to be added, which are aa[i][node.kk[i]]
        # if in any string there are no characters left use the gap symbol "-"
        next_characters = [self.words[i][node.kk[i]] if node.kk[i] < len(self.words[i]) else "-"
                           for i in range(len(self.words))]
        # get all combinations of possibilities to choose from next_characters
        combinations = [y for y in itertools.product([True, False], repeat=len(self.words))]
        # remove the characters to be added, which only consist of gaps
        combinations.remove((False,) * len(self.words))

        for comb in combinations:
            # get one new neighbor for each combination of True/False
            # if the corresponding index in comb is True, take the this character into the next node
            nodecc = [next_characters[i] if comb[i] else "-"
                      for i in range(len(next_characters))]
            # eliminate all only-gap character sequences
            if nodecc != ["-"] * len(self.words):
                # if comb[i] is true, we need to add 1 to the next nodes indices at the corresponding position
                # this is done only, if the i-th string has remaining characters
                nodekk = [node.kk[i] + int(comb[i]) if node.kk[i] != len(self.words[i]) else node.kk[i]
                          for i in range(len(next_characters))
                          ]
                # calculate the new present cost for the node
                gw = node.g + transitioncost(nodecc)
                # get remaining strings, which has not been aligned so far
                raaw = [self.words[j][nodekk[j]:] for j in range(len(self.words))]
                # calculate underestimation
                hw = self.underestimation(raaw)
                # put the neighbor into the PriorityQueue
                self.queue.put(Node(chars_column=nodecc, kk=nodekk, g=gw, h=hw, pred=node))

    def underestimation(self, raa):
        """
        raa are the rests of the strings to be aligned.
        """
        m = len(raa)
        estimation_sum = 0
        for i in range(m - 1):
            for j in range(i + 1, m):
                estimation_sum += self.lev(word_1=raa[i], word_2=raa[j])

        return estimation_sum

    def print_alignment(self, path: List[Node]):
        print("\n  Optimal Alignment A*: ")

        matrix = []
        for i in range(len(self.words)):
            matrix.append([x.chars_column[i] for x in path])

        print(tabulate(matrix))

    def lev(self, word_1, word_2):
        """
        Simplified LevDistance-Algorithm. This class only needs the score not the
        alignment of the rest of the strings
        """
        values_dic = {}
        word_1_length = len(word_1)
        word_2_length = len(word_2)

        for i in range(word_1_length + 1):
            values_dic[(i, 0)] = i
        for j in range(word_2_length + 1):
            values_dic[(0, j)] = j

        for i in range(1, word_1_length + 1):
            for j in range(1, word_2_length + 1):
                values_dic[(i, j)] = min([
                    values_dic[(i - 1, j)] + 1,
                    values_dic[(i, j - 1)] + 1,
                    values_dic[(i - 1, j - 1)] + int(word_1[i - 1] != word_2[j - 1])
                ])

        return values_dic[(word_1_length, word_2_length)]

    def msa(self):
        """
        The algorithm pops nodes out of the PriorityQueue until an end node is reached.
        """
        n: Node = self.queue.get(block=False)
        while not n.is_last(self.words):
            self.append_neighbors(node=n)
            n = self.queue.get(block=False)
        path = get_path(n)
        self.print_alignment(path)

        return n.f, get_path(n)
