
graph = {
    'S': ['A', 'D'],
    'A': ['B', 'C'],
    'B': ['E', 'C'],
    'C': ['G'],
    'D': ['B', 'E'],
    'E': ['G'],
    'G': []
}

visited = set()
path = []

def dfs(visited, graph, node, goal):
    if node not in visited:
        print(node)
        visited.add(node)
        path.append(node)
        if node == goal:
            return True

        for neighbour in graph[node]:
            if dfs(visited, graph, neighbour, goal):
                return True

        path.pop()

print("Following is the Depth-First Search:")
dfs(visited, graph, 'A', 'G')

print("Final Path:", path)