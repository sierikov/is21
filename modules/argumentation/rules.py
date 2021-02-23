def rebuts(a, b):
    return a.head.atom == b.head.atom and (a.head.isNeg != b.head.isNeg)


def undercuts(a, b):
    for bodyLiteral in b.body:
        if bodyLiteral.isDefault and bodyLiteral.objective == a.head.objective:
            return True
    return False


def attacks(a, b):
    return rebuts(a, b) or undercuts(a, b)


def defeats(a, b):
    return undercuts(a, b) or (rebuts(a, b) and not undercuts(b, a))


def strongly_attacks(a, b):
    return attacks(a, b) and not undercuts(b, a)


def strongly_undercuts(a, b):
    return undercuts(a, b) and not undercuts(b, a)
