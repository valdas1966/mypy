#=====================================================================
# Opened special Set for AStar
#=====================================================================
# Methods:
#---------------------------------------------------------------------
#   1. push(node)
#       Push Node into the Opened Set O(1).
#   2. pop()
#       Return the Best Node and Remove it from the Opened Set O(n).
#   3. is_empty()
#       Return True if the Opened Set is empty.
#   4. contains(node)
#       Return True if Opened Set contains Node.
#=====================================================================
# Edited: 11/09/2018
#=====================================================================
class Opened:
    

    #=================================================================
    # Constructor
    #=================================================================
    # Edited: 02/09/2018
    #=================================================================
    def __init__(self):
        self._opened = set()
        self._best = None
        
    
    #=================================================================
    # Push Node into the Opened Set
    #=================================================================
    # Complexity: O(1)
    #=================================================================
    # Edited: 10/09/2018
    #=================================================================
    def push(self, node):        
        self._opened.add(node)        
        self._update_best(node)                    
    
    
    #=================================================================
    # 1. Return the Best Node
    # 2. Remove it from the Opened Set
    #=================================================================
    # Complexity: O(n)
    #=================================================================
    # Edited: 02/09/2018
    #=================================================================
    def pop(self):        
        temp = self._best
        
        # Remove the Best Node from the Opened set
        #   and set the Best Node to be None
        if self._best is not None:
            self._opened.remove(self._best)
            self._best = None
            
        # Set the Best Node to be the minimum Node in the Opened
        for node in self._opened:
            self._update_best(node)
            
        return temp
    
    
    def remove(self, node):
        self._opened.remove(node)
        for node in self._opened:
            self._update_best(node)
    
    
    def contains(self,node):
        """
        ===================================================================
         Description: Return True if Opened Set contains the Node
        ===================================================================
         Arguments: node : Node (to check if exists in the Opened Set)
        ===================================================================
        """
        return node in self._opened
    
    
    #=================================================================
    # Return True if the Opened Set is empty
    #=================================================================
    # Edited: 01/09/2018
    #=================================================================
    def is_empty(self):
        return (len(self._opened) == 0)
    
    
    #=================================================================
    # Check the Node as candidate to be the Best Node
    #=================================================================
    # Complexity: O(1)
    #=================================================================
    # Edited: 10/09/2018
    #=================================================================
    def _update_best(self, node):
        if (self._best is None):
            self._best = node
        else:
            self._best = min(self._best,node)
            
    
    #=================================================================
    # List of Nodes where the Best Node is the first Node
    #=================================================================
    # Edited: 10/09/2018
    #=================================================================
    def __str__(self):
        if self.is_empty(): return 'Empty Opened'
        
        temp = '{}\n'.format(self._best)
        for node in self._opened:
            if (node != self._best):
                temp += '{}\n'.format(node)
        return temp
    
    
    
    
    
                
            
        