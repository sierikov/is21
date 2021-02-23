class Literal():
    """
    An objective literal is either au, r, a, d, sa, sun atom A or a negated atom neg A.
    A default literal has the form not L, where L is an objective literal.
    A literal is either a default or an objective literal.

    You can use attributes isDefault, isObjective, objective, isNeg, atom.
    """

    def __init__(self, s):
        s = s.strip()
        self.s = s
        self.isDefault = s.startswith("not")
        self.isObjective = not self.isDefault
        if self.isDefault:
            self.objective = s[3:].strip()
        else:
            self.objective = s
        self.isNeg = self.objective.startswith("-")
        if self.isNeg:
            self.atom = self.objective[1:]
        else:
            self.atom = self.objective

