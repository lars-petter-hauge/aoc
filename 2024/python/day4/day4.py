from pathlib import Path

TEST_INPUT="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def load():
    with open(Path(__file__).parent / "input.in") as fh:
        lines = fh.read()
    return lines

def parse_line(lines):
   return [[c for c in line] for line in lines if len(line)>1]


def indice_pairs(i,j,max_i, max_j,length):
    if i+length<=max_i:
        yield [(i+k, j) for k in range(length)]

    if i-length+1>=0:
        yield [(i-k, j) for k in range(length)]

    if j+length<=max_j:
        yield [(i, j+k) for k in range(length)]

    if j-length+1>=0:
        yield [(i, j-k) for k in range(length)]

    if j+length<=max_j and i+length<=max_i:
        yield [(i+k, j+k) for k in range(length)]

    if j-length+1>=0 and i-length+1>=0:
        yield [(i-k, j-k) for k in range(length)]

    if j+length<=max_j and i-length+1>=0:
        yield [(i-k, j+k) for k in range(length)]

    if j-length+1>=0 and i+length<=max_i:
        yield [(i+k, j-k) for k in range(length)]

def is_valid(ijpairs, max_i, max_j):
    return not any([i<0 or i>=max_i or j<0 or j>=max_j for i,j in ijpairs])

def cross_indices(i,j,max_i, max_j):
    indices = [(i-1,j-1),(i,j),(i+1,j+1)]
    if is_valid(indices, max_i, max_j):
        yield indices

    indices = [(i-1,j+1),(i,j),(i+1,j-1)]
    if is_valid(indices, max_i, max_j):
        yield indices
    
def solve(grid):
    number=0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]=="X":
                for indices in indice_pairs(i,j,len(grid),len(grid[0]), length=4):
                    word = "".join([grid[m][n] for m,n in indices])
                    if word == "XMAS":
                        number+=1
    return number

def solve_two(grid):
    number=0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]=="A":
                n_mas = 0
                indices = list(cross_indices(i,j,len(grid),len(grid[0])))
                for indice in indices:
                    word = "".join([grid[m][n] for m,n in indice])
                    if word == "MAS" or word == "SAM":
                        n_mas+=1
                if n_mas==2:
                    number+=1
    return number

print(solve(parse_line(load().split("\n"))))
print(solve_two(parse_line(load().split("\n"))))
