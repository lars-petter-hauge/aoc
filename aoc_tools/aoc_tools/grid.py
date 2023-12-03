import numpy as np
import itertools

DEFAULT_SYMBOL = {0: ".", 1: "#", 2: "O", 3: "H"}


def create_empty_grid(n_rows, n_cols):
    return np.zeros((n_rows, n_cols), dtype=int)


def grid_indices(grid):
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            yield (row, col)


def neighbour_indices(row, col, nrow, ncol, diagonals=True):
    for irow, icol in itertools.product([-1, 0, 1], repeat=2):
        if irow == 0 and icol == 0:
            continue
        if irow + row < 0 or icol + col < 0:
            continue
        if irow + row >= nrow:
            continue
        if icol + col >= ncol:
            continue
        if not diagonals and (irow, icol) in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            continue
        yield (irow + row, icol + col)


def neighbours(grid, row, col, diagonals=True):
    """Given a grid of:
    >>> grid = create_grid(5,5)
    >>> print_grid(grid)
    00000
    00000
    00000
    00000
    00000
    >>> indices = neighbour_indices(row=1, col=1, nrow=grid.shape[0], ncol=grid.shape[1])
    >>> for value, (row, col) in enumerate(indices,1):
    >>>     grid[row][col] = value
    >>> print_grid(grid
    12300
    40500
    67800
    00000
    00000

    If diagonals is False, only neighbour 2,4,5 and 8 will be returned
    >>> print(list(neighbours(grid,row=1, col=1, diagonals=False))
    [2,4,5,7]
    """
    for row, col in neighbour_indices(
        row, col, nrow=grid.shape[0], ncol=grid.shape[1], diagonals=diagonals
    ):
        yield grid[row][col]


def print_grid(grid, map_symbols=False, mapping=None):
    lines = []
    mapping = mapping or DEFAULT_SYMBOL
    for row in range(grid.shape[0]):
        line = ""
        for col in range(grid.shape[1]):
            symbol = grid[row][col]
            if map_symbols:
                symbol = mapping.get(symbol, symbol)
            line += str(symbol)
        lines.append(line)
    print("\n".join(lines))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
