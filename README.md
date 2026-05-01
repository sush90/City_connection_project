# City_connection_project

#Prism Algorithm:
This program finds the minimum cost to connect all nodes in a graph.
Used for the city cable-laying problem.

Algorithm Overview:
1. Start from any node
2. Repeatedly add the cheapest edge connecting a visited node to an unvisited node
3. Continue until all nodes are visited
4. Result: Minimum Spanning Tree (MST)

    Why this works?
    - Greedy algorithm: always pick cheapest available edge
    - Cut property: cheapest edge crossing any cut is in MST
    - Prim's maintains a single growing tree
    
    Data Structures:
    - visited (set): Track which nodes we've added to MST - O(1) lookup
    - min_heap (MinHeap): Priority queue of edges - O(log n) operations
    
    Time Complexity:
    - Each edge considered once: O(E)
    - Each edge pushed/popped from heap: O(log V)
    - Total: O((V + E) log V)
  
We used Custom Binary Min Heap Implementation
Used as priority queue for Prim's algorithm

A binary min heap is a complete binary tree where:
- Every parent node is smaller than its children
- The minimum element is always at the root (index 0)
- Stored as an array/list for efficiency
- 
    
