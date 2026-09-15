
def dls(graph, s, goal, l):         # Depth Limited Search
    if s == goal:                   # If first node is goal
        return s, [s]

    queue = [(s, 0, [s])]        # Queue Initialize (Node, depth, path)
    reached = {s}           # Reached set Initialize

    while queue:            # Until queue is not empty
        N, d, path = queue.pop()  # Take from top

        if d < l:               # Check if depth of N < current depth
            for R in graph[N]:
                if R not in reached:
                    new_path = path + [R]       # Making path

                    if R == goal:
                        return R, new_path

                    queue.append((R, d + 1, new_path))      # Add node to queue
                    reached.add(R)              # Mark node as reached

    return None


def ids(graph, s, goal):
    l = 0           # Initialize depth

    while True:
        result = dls(graph, s, goal, l)

        if result is not None:
            return result

        l =  l + 1


graph = {
    'S': ['A', 'B', 'C'],
    'A': ['D', 'E'],
    'B': ['G'],
    'C': ['F'],
    'D': ['H'],
    'E': [],
    'G': [],
    'F': [],
    'H': []
}

result = ids(graph, 'S', 'G')

print("\nGoal found:", result[0])
print("Path:", " -> ".join(result[-1]))