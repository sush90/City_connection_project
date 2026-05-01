## README - City Connections (MST Project)
## CSCI 311 - Spring 2026

KruskalAlgorithm.py  - MST using Kruskal's algorithm with a custom Disjoint Set Union (DSU)

prims.py             - MST using Prim's algorithm with a custom binary min-heap priority queue

min_heap.py          - Custom MinHeap class used by prims.py

Both programs read a weighted undirected graph from an input file, compute the Minimum
Spanning Tree (MST), and write the MST edges to an output file in the same format.

## HOW TO RUN

Kruskal's:
  python KruskalAlgorithm.py inputfile outputfile

Prim's:
  python prims.py inputfile outputfile

### Example:

  python KruskalAlgorithm.py SanJoaquin.txt kruskal_out.txt

  python prims.py SanJoaquin.txt prims_out.txt
