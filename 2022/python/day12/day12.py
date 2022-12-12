import itertools
import string
from collections import defaultdict, deque

PUZZLE_INPUT = """abcccccccaaaaaccccaaaaaaaccccccccccccccccccccccccccccccccccccaaaaa
abaacccaaaaaaccccccaaaaaaaaaaaaaccccccccccccccccccccccccccccaaaaaa
abaacccaaaaaaaccccaaaaaaaaaaaaaacccccccccccccaacccccccccccccaaaaaa
abaacccccaaaaaacaaaaaaaaaaaaaaaacccccccccccccaacccccccccccccacacaa
abaccccccaaccaacaaaaaaaaaacccaacccccccccccccaaacccccccccccccccccaa
abcccccccaaaacccaaaaaaaaacccccccccccccaaacccaaacccccccccccccccccaa
abccccccccaaaccccccccaaaacccccccccccccaaaaacaaaccacacccccccccccccc
abccccccccaaacaaacccccaaacccccccccccccaaaaaaajjjjjkkkcccccaacccccc
abcccccaaaaaaaaaacccccaaccccccccccciiiiiijjjjjjjjjkkkcaaaaaacccccc
abcccccaaaaaaaaacccccccccccccccccciiiiiiijjjjjjjrrkkkkaaaaaaaacccc
abcccccccaaaaaccccccccccccccccccciiiiiiiijjjjrrrrrppkkkaaaaaaacccc
abcccaaccaaaaaacccccccccccaacaaciiiiqqqqqrrrrrrrrpppkkkaaaaaaacccc
abccaaaaaaaaaaaaccccacccccaaaaaciiiqqqqqqrrrrrruuppppkkaaaaacccccc
abcccaaaaaaacaaaacaaacccccaaaaaahiiqqqqtttrrruuuuupppkkaaaaacccccc
abcaaaaaaaccccaaaaaaacccccaaaaaahhqqqtttttuuuuuuuuuppkkkccaacccccc
abcaaaaaaaaccccaaaaaacccccaaaaaahhqqqtttttuuuuxxuuuppkklcccccccccc
abcaaaaaaaacaaaaaaaaaaacccccaaachhhqqtttxxxuuxxyyuuppllllccccccccc
abcccaaacaccaaaaaaaaaaaccccccccchhhqqtttxxxxxxxyuupppplllccccccccc
abaacaacccccaaaaaaaaaaaccccccccchhhqqtttxxxxxxyyvvvpppplllcccccccc
abaacccccccccaaaaaaacccccccccccchhhpppttxxxxxyyyvvvvpqqqlllccccccc
SbaaccccccaaaaaaaaaaccccccccccchhhppptttxxxEzzyyyyvvvqqqlllccccccc
abaaaaccccaaaaaaaaacccccccccccchhhpppsssxxxyyyyyyyyvvvqqqlllcccccc
abaaaacccccaaaaaaaacccccccccccgggpppsssxxyyyyyyyyyvvvvqqqlllcccccc
abaaacccaaaacaaaaaaaccccccccccgggpppsswwwwwwyyyvvvvvvqqqllllcccccc
abaaccccaaaacaaccaaaacccccccccgggppssswwwwwwyyywvvvvqqqqmmmccccccc
abaaccccaaaacaaccaaaaccaaaccccggpppssssswwswwyywvqqqqqqmmmmccccccc
abcccccccaaacccccaaacccaaacaccgggpppssssssswwwwwwrqqmmmmmccccccccc
abcccccccccccccccccccaacaaaaacgggppooosssssrwwwwrrrmmmmmcccccccccc
abcccccccccccccccccccaaaaaaaacggggoooooooorrrwwwrrnmmmdddccaaccccc
abaccccccccccccaacccccaaaaaccccggggoooooooorrrrrrrnmmddddcaaaccccc
abaccccccccaaaaaaccccccaaaaaccccggfffffooooorrrrrnnndddddaaaaccccc
abaacccccccaaaaaacccccaaaaaacccccffffffffoonrrrrrnnndddaaaaaaacccc
abaaccccccccaaaaaaaccacaaaacccccccccffffffonnnnnnnndddaaaaaaaacccc
abccccccccccaaaaaaaaaaaaaaaccccccccccccfffennnnnnnddddccaaaccccccc
abcccccccccaaaaaaacaaaaaaaaaacccccccccccffeennnnnedddccccaaccccccc
abcccccccccaaaaaaccaaaaaaaaaaaccccccccccaeeeeeeeeeedcccccccccccccc
abccccccccccccaaaccaaaaaaaaaaaccccccccccaaaeeeeeeeecccccccccccccaa
abcccccccaaccccccccaaaaaaaacccccccccccccaaaceeeeecccccccccccccccaa
abaaccaaaaaaccccccccaaaaaaaacccccccccccccaccccaaacccccccccccaaacaa
abaaccaaaaacccccaaaaaaaaaaacccccccccccccccccccccacccccccccccaaaaaa
abaccaaaaaaaaccaaaaaaaaaaaaaacccccccccccccccccccccccccccccccaaaaaa"""

TEST_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def bfs(graph, start, end):
    path = {start: [start]}
    queue = deque([start])
    seen = set()
    while queue:
        node = queue.popleft()

        for sub_node in graph[node]:
            if sub_node == end:
                path[sub_node] = path[node] + [sub_node]
                return path[end]

            if sub_node in seen:
                continue
            path[sub_node] = path[node] + [sub_node]
            queue.append(sub_node)
            seen.add(sub_node)

    raise KeyError("Did not find end")


def neighbours(i, j, grid):
    if i > 0:
        yield (i - 1, j)
    if i < len(grid) - 1:
        yield (i + 1, j)
    if j > 0:
        yield (i, j - 1)
    if j < len(grid[0]) - 1:
        yield (i, j + 1)


def create_graph(grid):
    letters = ["S"]
    letters.extend(list(string.ascii_lowercase))
    letters.append("E")
    start = None
    end = None

    graph = defaultdict(list)
    for i, j in itertools.product(range(len(grid)), range(len(grid[0]))):
        cell_value = grid[i][j]
        if cell_value == "S":
            start = (i, j)
        if cell_value == "E":
            end = (i, j)
        for neighbour_i, neighbour_j in neighbours(i, j, grid):
            if (
                letters.index(cell_value)
                - letters.index(grid[neighbour_i][neighbour_j])
                >= -1
            ):
                graph[(i, j)].append((neighbour_i, neighbour_j))
    return graph, start, end


def print_map(heightmap, path):

    import time

    for i, j in path:
        print("\n".join(["".join(line) for line in heightmap]))
        print("\n")
        time.sleep(0.1)
        heightmap[i][j] = "#"


heightmap = [[c for c in line] for line in TEST_INPUT.split("\n")]
graph, start, end = create_graph(heightmap)
path = bfs(graph, start, end)
print(len(path))

heightmap = [[c for c in line] for line in PUZZLE_INPUT.split("\n")]
graph, start, end = create_graph(heightmap)
path = bfs(graph, start, end)

# Produces correct length for example and other users input, but is off by 2 for
# my input (i.e. off by 3 before removing start)
print(len(path) - 1)  # Remove start
