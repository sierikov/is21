from tabulate import tabulate

from modules.argumentation.rule import Rule


class Arguments:

    def __init__(self, fn):
        self.rules = self.read(fn)
        self.s = self.str(self.rules)

    def str(self, rules2, fallback=False):
        """Returns tabulate of all rules in rules2."""
        rules = [r.str() for r in rules2]
        if fallback and not len(rules):
            return "-- \nNo rule matches.\n--"

        return tabulate(rules)

    def str2(self, rules2):
        """Returns a string with all the heads of the rules in rules2."""
        return "{" + ", ".join([r.head.s for r in rules2]) + "}"

    def read(self, fn):
        """Reads rules from file fn."""
        rules = []
        for line in open(fn):
            r = Rule(line)
            rules.append(r)
        return rules

    def f(self, S, x, y):
        """Main function, which collected accetable arguments."""
        S2 = set([])
        for a in self.rules:
            if a.is_argument(S) and a.is_acceptable(S, x, y, self.rules):
                S2.add(a)
        return S2

    def justified(self, x, y):
        """Fixpoint semantics. Starting with the empty set, f is iteratively
        applied, until it reaches a fix point. In each step f computes the
        acceptable arguments wrt. the arguments accepted so far."""
        S = set([])
        i = 0
        f_S = self.f(S, x, y)
        while f_S != S:
            # print("\nIteration %d for %s/%s justified arguments"%(i,x.__name__,y.__name__))
            # print("f(%s) = %s"%(self.str2(S), self.str2(f_S)))
            i += 1
            S = f_S
            f_S = self.f(S, x, y)
        return S
