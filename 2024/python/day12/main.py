from collections import deque

TEST_INPUT = """AAAA
BBCD
BBCC
EEEC"""

TEST_INPUT_0 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""


TEST_INPUT_1 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

import sys

with open(sys.argv[1]) as fh:
    content = fh.readlines()

grid = [x.strip() for x in content]
grid = TEST_INPUT.split("\n")

NR = len(grid)
NC = len(grid[0])
regions = []
perimeter = 0
visited = set()
for r in range(NR):
    for c in range(NC):
        if (r, c) in visited:
            continue
        region = [(r, c)]
        visited.update([(r, c)])
        plant = grid[r][c]
        to_check = deque([(r, c)])

        fence = 0
        perimeter = 0
        while to_check:
            nr, nc = to_check.pop()
            unvisited_neighour = []
            visited_neighbours = []
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                cr = nr + dr
                cc = nc + dc
                if NR <= cr or cr < 0 or NC <= cc or cc < 0:
                    perimeter += 1
                    continue

                if (cr, cc) in region:
                    visited_neighbours.append([dr, dc])
                    continue

                if grid[cr][cc] == plant:
                    unvisited_neighour.append([dr, dc])
                    to_check.append((cr, cc))
                    region.append((cr, cc))
                    visited.update([(cr, cc)])
                else:
                    perimeter += 1
            if len(unvisited_neighour) + len(visited_neighbours) == 0:
                fence += 4
            elif len(unvisited_neighour) + len(visited_neighbours) == 1:
                if visited_neighbours:
                    fence += 3
                elif len(unvisited_neighour) == 1:
                    fence += 1
                else:
                    raise (ValueError)
            elif len(unvisited_neighour) + len(visited_neighbours) == 2:
                if sum(sum(item) for item in unvisited_neighour + visited_neighbours):
                    # in a straight line
                    fence += 0
                else:
                    fence += len(visited_neighbours)
            elif len(unvisited_neighour) + len(visited_neighbours) == 3:
                fence += 0

            print(nr, nc, unvisited_neighour, visited_neighbours)

        print(plant, fence)

        regions.append((plant, fence, perimeter, region))

print(sum([perim * len(reg) for _, _, perim, reg in regions]))

a = 4
