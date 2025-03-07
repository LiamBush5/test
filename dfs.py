#!/usr/bin/env python3

class Graph:
    def __init__(self):
        """
        Initialize your graph structure here.
        You can choose between:
        - Adjacency List (dictionary of lists/sets)
        - Adjacency Matrix (2D array/list)
        """
        self.graph = {}  # Adjacency list implementation

    def add_edge(self, u, v):
        """
        Add an edge to the graph.
        For undirected graph, add edges in both directions.
        """
        # Add edge from u to v
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

        # Add edge from v to u (for undirected graph)
        if v not in self.graph:
            self.graph[v] = []
        self.graph[v].append(u)

    def dfs(self, start_node):
        """
        Perform DFS traversal starting from start_node.
        Return the list of nodes in DFS order.
        """
        visited = set()  # To keep track of visited nodes
        result = []      # To store the DFS traversal order

        # Call the recursive helper function
        self._dfs_recursive(start_node, visited, result)

        return result

    def _dfs_recursive(self, node, visited, result):
        """
        Helper function for recursive DFS implementation.
        Example adj list
        {
        0: [1,2]
        1: [0,1]
        2: [4,2]
        3: [4,5]
        4: [2,3]
        5: [3]
        6: [7]
        7: [6]
        8: [9]
        9: [8]
        10: []
        }
        """
        # Mark the current node as visited and add to result
        visited.add(node)
        result.append(node)

        # Recur for all adjacent vertices
        if node in self.graph:
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    self._dfs_recursive(neighbor, visited, result)

    def dfs_iterative(self, start_node):
        """
        Iterative implementation of DFS using a stack.
        """
        visited = set()
        result = []
        stack = [start_node]

        while stack:
            # Pop a vertex from stack
            node = stack.pop()

            # If not visited, mark it as visited and add to result
            if node not in visited:
                visited.add(node)
                result.append(node)

                # Add all unvisited neighbors to stack
                if node in self.graph:
                    # Add neighbors in reverse order to match recursive DFS
                    for neighbor in reversed(self.graph[node]):
                        if neighbor not in visited:
                            stack.append(neighbor)

        return result


# Example usage:
if __name__ == "__main__":
    # Create a sample graph
    g = Graph()

    # Add edges to create a sample graph
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]
    for u, v in edges:
        g.add_edge(u, v)

    # Perform DFS using recursive approach
    print("DFS traversal (recursive) starting from node 0:")
    print(g.dfs(0))

    # Perform DFS using iterative approach
    print("DFS traversal (iterative) starting from node 0:")
    print(g.dfs_iterative(0))

    # You can also test with different graph structures:
    # 1. A simple path
    # 2. A cycle
    # 3. A disconnected graph
    # 4. A tree structure
    # 5. A complete graph
