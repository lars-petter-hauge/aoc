import sys
from collections import deque

with open(sys.argv[1]) as fh:
    content = fh.readlines()

TEST_INPUT="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

TEST_INPUT=""".....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9...."""

def parse_content(content):
    return [[int(c) if c.isdigit() else c for c in line.strip()] for line in content]

def solve(grid):
    NR = len(grid)
    NC = len(grid[0])
    to_visit = deque()
    part_one = {}
    part_two = {}
    for r in range(NR):
        for c in range(NC):
            if grid[r][c]!= 0:
                continue
            to_visit.append(((r,c), 0))
            
            reachable_heads = set()
            num_paths = 0
            while to_visit:
                (cr,cc),val = to_visit.popleft() 
                if val == 9:
                    reachable_heads.update(set([(cr,cc)]))
                    num_paths +=1
                else:
                    for dr, dc in ((cr-1,cc),(cr+1,cc), (cr,cc-1),(cr,cc+1)):
                        if dr<0 or dc < 0 or dr >= NR or dc >= NC:
                            continue
                        if grid[dr][dc] == val+1:
                            to_visit.append(((dr,dc),val+1))
            part_one[(r,c)]=reachable_heads
            part_two[(r,c)]=num_paths 
    return part_one, part_two


result, second_result = solve(parse_content(TEST_INPUT.split("\n")))
result,second_result = solve(parse_content(content))
print(sum([len(val) for _,val in result.items()]))
print(sum([val for _,val in second_result.items()]))
