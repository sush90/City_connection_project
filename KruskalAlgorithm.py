import time
import sys

"""
Minimum Spanning Tree (MST) using Kruskal's Algorithm.
"""

class DSU:
    """
    Disjoint Set Union data structure.

    find - determine the representative (root) of a node's set
    union - merge the sets containing two nodes

    
    Optimizations:
    Union by rank: always attatches the shallower tree under the deeper tree
                    keeping trees flat and find() fast
    Path compression (iterative): after find() locates the root, 
                    every node visted along the way is re-linked directly to root

                    
    Attributes:
        parent (dict): Maps each node to its current parent.

        rank (dict): Upper-bound estimate of the subtree height rooted at each node
                        Used by uniont() to decide attatcment order
    """
    def __init__(self, nodes):
        """
        Initialize the DSU so every node is its own single set
        Args:
            nodes: collection of node identiffiers 
        """
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, i):
        """
        Return the root (representative) of the set containg node i

        Uses iterative paths compression: after the root is found, 
        every node on the path form i to the root is re-pointed to root.

        Args:
            i: A node that was passed to __init__
        Returns:
            The root node of the set containing i
        """
        root = i
        # Walk up to find the actual root
        while self.parent[root] != root:
            root = self.parent[root]
    
        # Path Compression (Iterative)
        # re-link every node on the path directly to root
        while self.parent[i] != root:
            next_node = self.parent[i]
            self.parent[i] = root
            i = next_node
            
        return root
    
    def union(self, i, j):
        """
        Merge the sets containing node i and j
        The root of the shallower tree is attatched under the root of the deeper tree to minimize the height increase.
        When both trees have equal rank the second root become the new combined root and rank is incremented by one.

        Args:
            i: A node in the first set
            j: A node in the second set
        Returns:
            bool: True - nodes were in different sets and now are merged
                    False - the nodes were already in the same set (adding would create a cycle)
        """
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Always attach the shorter tree to the taller one
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            return True
        return False
    
def run_kruskals():
    """
    Algorithm Overview:
        1. Read a weighted, undirected graph from a file
        2. Sort all edges by weight
        3. Greedily add edge to the MST if it doesn't form a cylce
            Cycle detection is handled efficiently by a Disjoint Set Union (DSU)
        4. Write the result MST edges to an output file 
    """

    # validation
    if len(sys.argv) < 3:
        print("Usage: python program.py <intputfile> <outputfile>")
        return
        
    # path to the input graph file
    input_filename = sys.argv[1]
    # path for the output MST file 
    output_filename = sys.argv[2]
    
    start_total = time.time()

    # Reading file ---- Parase input file
    # each accepted line yields to one tuple (weight, edge_idf, node_u, node_v)
    # tupples sorted in 'edges'
    # lightest edge first
    start_parse = time.time()
    edges = []
    nodes = set()
    try:
        with open(input_filename, 'r') as f:
            for line in f: 
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()

                e_id = parts[0]         # edge identifier
                u = int(parts[1])       # source node
                v = int(parts[2])       # destination node
                dis = float(parts[3])   # edge weight/ distance

                
                edges.append((dis, e_id, u, v))
                nodes.add(u)
                nodes.add(v)

    except FileNotFoundError:
        print(f"Error: {input_filename} not found.")
        return
    end_parse = time.time()
    
    # Sort edges by wieght (smallest to largest)
    start_sort = time.time()
    edges.sort()
    end_sort = time.time()

    # ----- Kruskal's logic ------
    # iterate over sorted edges: add an edge to the MST only when its two
    # endpoints belong to different components
    # when |V| - 1 edges added then MST complete
    start_algo = time.time()
    dsu = DSU(nodes)
    mst_results = []
    total_weight = 0.0

    for dist, e_id, u, v in edges:
        if dsu.union(u, v):
            mst_results.append(f"{e_id} {u} {v} {dist}")
            total_weight += dist
    end_algo = time.time()

    # write output file - MST edges
    with open(output_filename, 'w') as f:
        for line in mst_results:
            f.write(line + "\n")

    end_total = time.time()


    # Print summary 
    print(f"Success! MST saved to {output_filename}")
    print("-" * 30)
    print(f"MST RESULTS FOR: {input_filename}")
    print(f"Edges in MST:    {len(mst_results)}")
    print(f"Total MST Weight: {total_weight:.6f}")
    print("-" * 30)
    print(f"TIME BREAKDOWN:")
    print(f"Parsing Time:    {end_parse - start_parse:.4f}s")
    print(f"Sorting Time:    {end_sort - start_sort:.4f}s")
    print(f"Algorithm Time:  {end_algo - start_algo:.4f}s")
    print(f"TOTAL RUNTIME:   {end_total - start_total:.4f}s")
    print("-" * 30)

if __name__ == '__main__':
    run_kruskals()