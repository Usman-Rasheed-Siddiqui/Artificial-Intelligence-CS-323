
graph = {
    'S': ['A', 'D'],
    'A': ['B', 'C'],
    'B': ['C', 'E'],
    'C': ['G'],
    'D': ['B', 'E'],
    'E': ['G'],
    'G': []
}

visited = []
queue = []
parent = {}


def bfs(visited, graph, node, goal):
    visited.append(node)
    queue.append(node)
    print("Reached nodes:", end=' ')
    parent[node] = None

    while queue:
        m = queue.pop(0)
        print(f'{m}', end=" ")
        if m == goal:
            break

        for neighbour in graph[m]:
            if neighbour not in visited:
                parent[neighbour] = m
                visited.append(neighbour)
                queue.append(neighbour)

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    print("\nFinal Path:", path)

# Driver Code
print("Following is the Breadth-First Search")
bfs(visited, graph, 'A', 'G') # function calling