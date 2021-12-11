from collections import deque

input_tree = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F", "G"]}

def BFS(graph, start):
    queue = deque()
    queue.append(start)
    seen = list()
    while queue:
        node = queue.popleft()
        if node in graph:
            nodes = graph[node]
            queue.extend(nodes)
        seen.append(node)
    return seen


def DFS(graph, start):
    queue = deque()
    queue.append(start)
    seen = list()
    while queue:
        node = queue.pop()
        if node in graph:
            nodes = graph[node]
            queue.extend(nodes)
        seen.append(node)
    return seen

print(BFS(input_tree, "A"))
print(DFS(input_tree, "A"))