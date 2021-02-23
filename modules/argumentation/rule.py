from modules.argumentation.literal import Literal


class Rule:
    """
    A rule has a head and a body. The head is an objective literal.
    The body is either empty or consists of objective and default literals.
    Syntax: head <- L1, not L2, ...
    """

    def __init__(self, s):
        s = s.strip()
        self.s = s
        # remove dot at the end of the string and split at <-
        l = s.rstrip(".").split("<-")
        self.head = Literal(l[0])
        if l[1]:
            # split body string at commas and convert items to literal using map.
            self.body = list(map(lambda x: Literal(x), l[1].split(",")))
        else:
            self.body = []

    def is_argument(self, S):
        """A rule is an argument if the objective literals in its body are in S.
        This means, there were rules for these objective literals, as required
        by the formal definition of an argument. Also the default literals in the
        body is must not yet be accepted."""
        for bodyLiteral in self.body:
            if bodyLiteral.isObjective and bodyLiteral.objective not in map(lambda x: x.head.objective, list(S)):
                return False
        return True

    def exists_argument(self, S, y, b):
        """There is an accepted argument in S, which y-attacks argument b"""
        for c in S:
            if y(c, b):
                return True
        return False

    def is_acceptable(self, S, x, y, arguments):
        """An argument a is acceptable if for all b, which  x-attack a,
        there is an accepted argument c, which y-attacks b."""
        for b in arguments:
            if x(b, self) and not self.exists_argument(S, y, b):
                return False
        return True

    def str(self):
        """Return a list of head and body string for use in tabulate."""
        return [self.head.s, "<-", ", ".join(map(lambda x: x.s, self.body)), "."]
