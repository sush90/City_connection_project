"""
This program finds the minimum cost to connect all nodes in a graph.
Used for the city cable-laying problem.
"""

import sys
import time
from min_heap import MinHeap

#File I/O
def read_graph(filename):
    """
    Read graph from file in edge list format.
    Input file format (one edge per line):
        edge_id start_node end_node weight
    Returns:
        edges: List of tuples (edge_id, start, end, weight)
        nodes: Set of all node IDs
    """
    edges = []
    nodes = set()
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse line
            parts = line.split()
            edge_id = int(parts[0])
            start = int(parts[1])
            end = int(parts[2])
            weight = float(parts[3])
            
            # Store edge and nodes
            edges.append((edge_id, start, end, weight))
            nodes.add(start)
            nodes.add(end)
    
    return edges, nodes


def write_output(filename, mst_edge_ids, original_edges):
    """
    Write MST edges to output file in same format as input.
    Args:
        filename: Path to output file
        mst_edge_ids: List of edge IDs in the MST
        original_edges: Original edge list to look up edge data
    """
    # Create dictionary for fast lookup
    edge_dict = {edge_id: (edge_id, start, end, weight) 
                 for edge_id, start, end, weight in original_edges}
    
    with open(filename, 'w') as f:
        # Write edges in sorted order for consistency
        for edge_id in sorted(mst_edge_ids):
            if edge_id in edge_dict:
                eid, start, end, weight = edge_dict[edge_id]
                f.write(f"{eid} {start} {end} {weight}\n")


#GRAPH REPRESENTATION

def build_adjacency_list(edges):
    """
    Build adjacency list representation from edge list.
    Adjacency List: For each node, store list of (neighbor, weight, edge_id)
    Args:
        edges: List of (edge_id, start, end, weight)
    Returns:
        graph: Dictionary mapping node_id -> list of (neighbor, weight, edge_id)
    """
    graph = {}
    
    for edge_id, start, end, weight in edges:
        # Initialize node lists if needed
        if start not in graph:
            graph[start] = []
        if end not in graph:
            graph[end] = []
        
        # Add edge to both nodes (undirected graph)
        graph[start].append((end, weight, edge_id))
        graph[end].append((start, weight, edge_id))
    
    return graph


# PRIM'S ALGORITHM 

def prims_mst(graph, start_node):
    """
    Prim's algorithm to find Minimum Spanning Tree.
    Args:
        graph: Adjacency list representation
        start_node: Node to start from (any node works)
    Returns:
        mst_edges: List of edge IDs in the MST
        total_weight: Sum of weights in MST
    """
    # Track which nodes are in the MST
    visited = set()
    
    # Priority queue: (weight, node, edge_id)
    # Start with starting node (weight 0, no incoming edge)
    min_heap = MinHeap()
    min_heap.push((0, start_node, None))
    
    # MST results
    mst_edges = []
    total_weight = 0
    
    # Process until all nodes visited or queue empty
    while not min_heap.is_empty():
        # Get cheapest edge to an unvisited node
        weight, node, edge_id = min_heap.pop()
        
        # Skip if already visited (duplicate in queue)
        if node in visited:
            continue
        
        # Add node to MST
        visited.add(node)
        
        # Add edge to MST (skip first node which has no incoming edge)
        if edge_id is not None:
            mst_edges.append(edge_id)
            total_weight += weight
        
        # Add all edges from this node to unvisited neighbors
        if node in graph:
            for neighbor, edge_weight, eid in graph[node]:
                if neighbor not in visited:
                    min_heap.push((edge_weight, neighbor, eid))
    
    return mst_edges, total_weight


# MAIN PROGRAM
def main():
    if len(sys.argv) != 3:
        print("Usage: python prisms.py inputfile outputfile")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # START TIMING
    total_start = time.time()
    
    # Read graph
    print(f"Reading graph from {input_file}...")
    read_start = time.time()
    edges, nodes = read_graph(input_file)
    read_end = time.time()
    print(f"  Graph has {len(nodes)} nodes and {len(edges)} edges")
    
    # Build adjacency list
    print("Building adjacency list...")
    build_start = time.time()
    graph = build_adjacency_list(edges)
    build_end = time.time()
    
    # Run Prim's algorithm
    print("Running Prim's algorithm...")
    prim_start = time.time()
    start_node = min(nodes)
    mst_edges, total_weight = prims_mst(graph, start_node)
    prim_end = time.time()
    
    # Validate
    expected_edges = len(nodes) - 1
    print(f"  MST contains {len(mst_edges)} edges (expected {expected_edges})")
    print(f"  Total MST weight: {total_weight:.2f}")
    
    if len(mst_edges) != expected_edges:
        print("  WARNING: MST edge count doesn't match!")
    
    # Write output
    print(f"Writing output to {output_file}...")
    write_start = time.time()
    write_output(output_file, mst_edges, edges)
    write_end = time.time()
    
    # END TIMING
    total_end = time.time()
    
    #PRINT TIMING RESULTS
    print("\n" + "="*50)
    print("PERFORMANCE BREAKDOWN")
    print("="*50)
    print(f"Reading file:      {read_end - read_start:8.4f}s")
    print(f"Building graph:    {build_end - build_start:8.4f}s")
    print(f"Prim's algorithm:  {prim_end - prim_start:8.4f}s  ← CORE ALGORITHM")
    print(f"Writing output:    {write_end - write_start:8.4f}s")
    print("-"*50)
    print(f"TOTAL TIME:        {total_end - total_start:8.4f}s")
    print("="*50)
    
if __name__ == "__main__":
    main()

  
