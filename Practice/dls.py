
def dls(node, goal, length, graph):
    if node == goal:
        return node, [node]

    queue = [(node, 0, [node])]
    reached = {node}

    while queue:
        N, d, path = queue.pop()

        if d < length:
            for successor in graph[N]:
                if successor not in reached:

                    newpath = path + [successor]
                    reached.add(successor)
                    queue.append((successor, d + 1, newpath))

                    if successor == goal:
                        return successor, newpath

    return None

def ids(graph, node, goal):
    length = 0
    while True:
        result = dls(node, goal, length, graph)

        if result is not None:
            return result

        length += 1


graph = {
    'S': ['A', 'D'],
    'A': ['B', 'C'],
    'B': ['E', 'C'],
    'C': ['G'],
    'D': ['B', 'E'],
    'E': ['G'],
    'G': []
}

result = ids(graph, 'A', 'G')

print('Goal found', result[0])
print("Path:", " -> ".join(result[-1]))




    