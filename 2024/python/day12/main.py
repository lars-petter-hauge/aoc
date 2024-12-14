from collections import deque
import sys

TEST_INPUT="""AAAA
BBCD
BBCC
EEEC"""



with open(sys.argv[1]) as fh:
    content = fh.readlines()

grid = TEST_INPUT.split("\n")

NR = len(grid)
NC = len(grid[0])

regions = []
visited = set()
for r in range(NR):
    for c in range(NC):
        if (r,c) in visited:
            continue
        region = [(r,c)]
        to_check = deque(grid[r][c])
        while to_check:
            plant = to_check.pop()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                cr = r+dr
                cc = c+dc
                if NR<=cr or cr<0 or NC<=cc or cc<0 or (r,c) in visited:
                    continue
                if grid[cr][cc] == plant:
                    region.append((cr,cc))
                    visited.update([(cr,cc)])
        print(plant)
        print(region)
        regions.append(region)

a=4

        
