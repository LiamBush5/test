#!/usr/bin/env python3

def print_graph_structure():
    # The adjacency list representation of the graph
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 4],
        3: [1, 4],
        4: [2, 3]
    }

    print("Graph Structure (Adjacency List):")
    print("--------------------------------")
    for node, neighbors in graph.items():
        print(f"Node {node} is connected to: {neighbors}")

    print("\nText Representation of the Graph:")
    print("--------------------------------")
    print("    0")
    print("   / \\")
    print("  1   2")
    print("  |   |")
    print("  3---4")
    print("\nDFS Traversal Path (starting from node 0):")
    print("--------------------------------")
    print("0 → 1 → 3 → 4 → 2")

    print("\nExplanation of DFS Traversal:")
    print("--------------------------------")
    print("1. Start at node 0")
    print("2. Visit first neighbor: node 1")
    print("3. Visit first unvisited neighbor of node 1: node 3")
    print("4. Visit first unvisited neighbor of node 3: node 4")
    print("5. All neighbors of node 4 (nodes 2 and 3) have been visited or are being processed")
    print("6. Backtrack to node 0 and visit its second neighbor: node 2")
    print("7. All nodes have been visited, DFS is complete")

if __name__ == "__main__":
    print_graph_structure()