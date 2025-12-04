import sys

TEST = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


content = sys.stdin.read()
# content = TEST
grid = [[c for c in line] for line in content.splitlines()]


def get_neighbours(i, j, length):
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < length - 1:
        yield i + 1, j
    if j < length - 1:
        yield i, j + 1
    if i > 0 and j > 0:
        yield i - 1, j - 1
    if i < length - 1 and j < length - 1:
        yield i + 1, j + 1
    if i > 0 and j < length - 1:
        yield i - 1, j + 1
    if i < length - 1 and j > 0:
        yield i + 1, j - 1


def removeable_papers(grid):
    papers = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "@":
                continue
            distractions = 0
            for m, n in get_neighbours(i, j, len(grid)):
                if grid[m][n] == "@":
                    distractions += 1
            if distractions < 4:
                papers.append([i, j])
    return papers


p1 = removeable_papers(grid)
print(len(p1))

p2 = []
while True:
    papers = removeable_papers(grid)
    if len(papers) == 0:
        break
    for i, j in papers:
        grid[i][j] = "."
    p2.extend(papers)

print(len(p2))
