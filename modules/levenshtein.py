def calc_distance(first: str, second: str, table: bool = False):
    row: int = len(first)
    col: int = len(second)
    d: dict = {}
    for i in range(0, row + 1):
        d[(i, 0)] = i
    for j in range(0, col + 1):
        d[(0, j)] = j
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            # delta is 1 iff mismatch of characters
            delta = int(first[i - 1] != second[j - 1])
            d[(i, j)] = min(d[(i - 1, j)] + 1,
                            d[(i, j - 1)] + 1,
                            d[(i - 1, j - 1)] + delta)
    matrix = [[0 for _ in range(col + 1)] for _ in range(row + 1)]
    for key, value in d.items():
        matrix[key[0]][key[1]] = value
    if table:
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    print('Distance is %d' % matrix[row][col])
    return d[(row, col)]
