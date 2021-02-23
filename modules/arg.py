from modules.argumentation.arguments import Arguments
from modules.argumentation.rules import attacks, undercuts, defeats, strongly_undercuts, strongly_attacks, rebuts


def calc_arg(file_path: str,
             show_data: bool,
             show_rebut: bool,
             show_attacks: bool,
             show_defeats: bool,
             show_undercuts: bool,
             show_strong_attacks: bool,
             show_strong_undercuts: bool,
             show_all: bool):
    args = Arguments(file_path)
    all = [["", "x", "y", "Justified arguments"]]
    notions_of_attack = []
    if show_data:
        print("\nRules:\n%s\n" % args.s)

    if show_rebut:
        notions_of_attack.append(rebuts)

    if show_attacks:
        notions_of_attack.append(attacks)

    if show_defeats:
        notions_of_attack.append(defeats)

    if show_undercuts:
        notions_of_attack.append(undercuts)

    if show_strong_attacks:
        notions_of_attack.append(strongly_attacks)

    if show_strong_undercuts:
        notions_of_attack.append(strongly_undercuts)

    if show_all:
        notions_of_attack.clear()
        notions_of_attack = [undercuts, attacks, defeats, strongly_undercuts, strongly_attacks]

    # Check all of the following notions of attack, as defined above
    i = 0

    # Check all combintations of notions of attack for proponent and opponent
    for x in notions_of_attack:
        for y in notions_of_attack:
            i += 1
            # Compute the justified arguments
            just = args.justified(x, y)
            # And print them nicely
            str_rule = (x.__name__, y.__name__, args.str(just, fallback=True))
            print("\n\nJustified arguments for x=%s and y=%s:\n%s\n" % str_rule)
            all.append([i, x.__name__, y.__name__, ", ".join(map(lambda x: x.head.s, just))])


