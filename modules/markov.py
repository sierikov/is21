from tabulate import tabulate


def calc_hmm(file_path: str, show_transitions: bool, show_emissions: bool, show_data: bool, sentence: str, start: str, end: str):
    (transition, emission) = read_training(file_path, show_data)

    if show_transitions:
        show_transition(transition)

    if show_emissions:
        show_emission(emission)

    if sentence != "":
        detect_words(sentence, transition, emission, start, end)


def detect_words(sentence: str, transition, emission, start, end):
    viterbi_alg(start + " " + sentence + " " + end, transition, emission)


def show_transition(transition):
    show("Transitions", transition)


def show_emission(emission):
    show("Emissions", emission)


def show(name: str, data):
    print("- %s:" % name)
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for ((s, o), v) in sorted_data:
        print("%s -> %s: %0.2f" % (s, o, v))


class Prob:
    """Counts occurrences for a pair of keys (either state to state or state to observation)
    as well as frequency of first state overall. Output are probability to transition."""

    def __init__(self):
        self.c = {}
        self.n = {}
        self.p = {}

    def inc(self, k1, k2):
        self.c[(k1, k2)] = self.c.get((k1, k2), 0) + 1
        self.n[k1] = self.n.get(k1, 0) + 1

    def prob(self):
        for (k1, k2) in self.c:
            self.p[(k1, k2)] = float(self.c[(k1, k2)]) / float(self.n[k1])
        return self.p


def max_pos(l):
    """Returns the maximum and its position."""
    m = max(l)
    return l.index(m), m


def viterbi_alg(str, transition, emission):
    viterbi = {}  # dynamic programming matrix
    pos = {}  # matrix to record path for backtracking
    obs = str.split()
    obs = [o.replace(".", "") for o in obs]
    states = list(set([s for (s, o) in emission]))

    # Init
    for s in states:
        viterbi[(s, 0)] = float(s == "S")
        # Fill matrix
    for i in range(1, len(obs)):
        for j in states:
            # Fji = max F(r,i-1)*A(r,j)*B(j,i)
            (pos[(j, i)], viterbi[(j, i)]) = max_pos(
                [viterbi[(r, i - 1)] * transition.get((r, j), 0.0) * emission.get((j, obs[i]), 0.0) for r in states])
    # Output table
    table = [[""] + obs]
    for s in states:
        row = [s]
        for i in range(len(obs)):
            row.append(viterbi[(s, i)])
        table.append(row)
    s = "E"
    seq = ["E"]
    for i in range(len(obs) - 1, 0, -1):
        s = states[pos[(s, i)]]
        seq.insert(0, s)
    table.append([""] + seq)
    print()
    print(tabulate(table, headers="firstrow"))


def read_training(fn, show_data):
    """Data format: First word represents state sequence. Remaining words are observations.
   For each character in the first word, there must be a word following.
    Start state is S, End state is E
    """
    t = Prob()
    e = Prob()
    if show_data:
        print("- HMM is trained on the following data:")
    for line in open(fn):
        if show_data:
            print(line.strip())
        l = line.split()
        seq = list(l[0])
        obs = l[1:]
        if len(seq) != len(obs):
            print("Format error in line %s" % line)
        else:
            # Count transitions
            for i in range(len(seq) - 1):
                t.inc(seq[i], seq[i + 1])
            # Count emissions
            for i in range(len(seq)):
                e.inc(seq[i], obs[i])
    return t.prob(), e.prob()
