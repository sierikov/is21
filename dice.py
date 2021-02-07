def calc_dice(first: str, second: str, show: bool):
    first_trigrams = calc_trigrams(first)
    second_trigrams = calc_trigrams(second)
    if show:
        print('Amount of trigrams:')
        print('- %s -> %f' % (first, len(first_trigrams)))
        print('- %s -> %f' % (second, len(second_trigrams)))
    dice: float = 2 * len(first_trigrams & second_trigrams) / (len(first_trigrams) + len(second_trigrams))
    print('Dice coefficient is %f' % dice)
    return dice


def calc_trigrams(word: str):
    return set([word[i:i + 3] for i in range(len(word) - 2)])
