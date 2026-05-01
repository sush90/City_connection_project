"""
Custom Binary Min Heap Implementation
Used as priority queue for Prim's algorithm
"""

class MinHeap:
    """
    - push(item): Add item to heap 
    - pop(): Remove and return minimum item
    - is_empty(): Check if heap is empty
    """
    
    def __init__(self):
        self.heap = []
    
    def push(self, item):
        """
        Add item to heap and maintain heap property.
        Args:
            item: Tuple (priority, data) where priority determines ordering
        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
    
    def pop(self):
        """
        Remove and return the minimum item (root).
        Returns:
            The minimum item, or None if heap is empty
        """
        if len(self.heap) == 0:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # Swap first and last elements
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        min_item = self.heap.pop()
        
        # Restore heap property
        if len(self.heap) > 0:
            self._sift_down(0)
        
        return min_item
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def _sift_up(self, index):
        """
        Move item up the tree to restore heap property. 
        Args:
            index: Position of item to sift up
        """
        parent_index = (index - 1) // 2
        
        # If not at root and smaller than parent, swap
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = \
                self.heap[parent_index], self.heap[index]
            self._sift_up(parent_index)
    
    def _sift_down(self, index):
        """
        Move item down the tree to restore heap property.  
        Args:
            index: Position of item to sift down
        """
        min_index = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        
        # Find smallest among node and its children
        if left_child < len(self.heap) and \
           self.heap[left_child] < self.heap[min_index]:
            min_index = left_child
        
        if right_child < len(self.heap) and \
           self.heap[right_child] < self.heap[min_index]:
            min_index = right_child
        
        # If smallest is not current node, swap and continue
        if min_index != index:
            self.heap[index], self.heap[min_index] = \
                self.heap[min_index], self.heap[index]
            self._sift_down(min_index)