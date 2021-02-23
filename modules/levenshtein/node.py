from typing import List


class Node:
    """
    Node class for the A*-Search.
    Consists of a column of characters. Each node is also characterized by the
    present cost, by the underestimated cost to the aim and by the total cost g + h.
    Furthermore we have "pointer" k1, k2... , which points to the character in the total strings to be aligned,
    which needs to be added next. If the strings to be aligned have lengths i1, i2 ... the final states are
    characterized by the condition i1 == k1.
    The method __lt__ needs to be defined in order to implement an order on the nodes, which is necessary for dealing
    with the PriorityQueue.
    """

    def __init__(self, chars_column: List[str], kk: List[int], g: int, h: float, pred: 'Node'):
        self.chars_column = chars_column
        self.kk = kk
        self.h = h
        self.g = g
        self.f = g + h
        self.pred = pred

    def __lt__(self, other: 'Node'):
        return self.f < other.f

    def is_last(self, aa: List[str]):
        return self.kk == [len(aa[i]) for i in range(len(aa))]
