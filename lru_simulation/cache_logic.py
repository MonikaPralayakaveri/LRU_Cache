from __future__ import annotations
from typing import Any, Optional

class Node:
    """A single cell in our DLL."""
    def __init__(self, key: str, value: Any):
        self.key: str = key
        self.value: Any = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class DoublyLinkedList:
    """
    Manages Node recency.
    Head.next is the 'Hot' (MRU) end.
    Tail.prev is the 'cold' (LRU) end.
    """
    def __init__(self):
        #create dummy boundaries
        self.head: Node = Node("__head__", None)
        self.tail: Node = Node("__tail__", None)

        #connect them to each other
        self.head.next = self.tail
        self.tail.prev = self.head

        self.size: int = 0
    
    def add_to_front(self, node: Node) -> None:
        """Squeezes a node between the head and the first real node."""
        # Step A: Identify the current first node
        first_node = self.head.next
        
        # Step B: Make our new node point to its new neighbors
        node.next = first_node
        node.prev = self.head
        
        # Step C: Make neighbors point back to our new node
        self.head.next = node
        if first_node:
            first_node.prev = node
        
        self.size += 1
    def remove_node(self, node: Node) -> None:
        """Unlinks a node from its current neighbors."""
        prev_node = node.prev
        next_node = node.next

        #make the neighbors point to each other, byPASSING 'Node'
        if prev_node:
            prev_node.next =next_node
        if next_node:
            next_node.prev = prev_node

        self.size -= 1

    def move_to_front(self, node: Node) -> None:
        """Moves an existing node to the front (MRU)."""
        #we already know wrote the core logic! just combine them:
        self.remove_node(node)
        self.add_to_front(node)

    def remove_tail(self) -> Optional[Node]:
        """Removes and returns the LRU node (the one before tail)."""
        if self.size == 0:
            return None

        #The true LRU node is the one just right before the dummy tail
        
        lru_node = self.tail.prev
        
        #safety check: make sure we didn't accidentally grab the dummy head

        if lru_node and lru_node != self.head:
            self.remove_node(lru_node)
            return lru_node
        return None

    def __len__(self) -> int:
        """Allow us to use len(my_list)."""
        return self.size

class LRUCache:
    """
    The "Brain" of the OS.
    Uses a Dictionary for O(1) lookups and a DLL to track recency.
    """
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.cache: dict[str, Node] = {} #The "Index (Hash map)"
        self.list: DoublyLinkedList = DoublyLinkedList() #the order


    def get(self, key: str) -> Optional[Any]:
        """Check if key exists. If yes, move to front and return value. If no, return None"""
        if key not in self.cache:
            return None

        #O(1) Lookup: Jump Straight to the Node!
        node = self.cache[key]

        #O(1) Update: Move it to the front of the Hot End!
        self.list.move_to_front(node)

        return node.value

    def put(self, key: str, value: Any) -> Optional[str]:
        """Add or updates an item. If cache is full, evicts the LRU item returns the key of the evicted item"""

        evicted_key = None

        if key in self.cache:
            #SCENARIO 1: It is already exists
            #update the data and refresh its recency!
            node = self.cache[key]
            node.value = value
            self.list.move_to_front(node)
        else:
            #SCENARIO 2:It's new data.(page replacement happens)
            #Check if we are full
            if len(self.list) >= self.capacity:

                #snip the oldest card from the Timeline(DLL)
                lru_node = self.list.remove_tail()

                if lru_node:
                    #crucial step: Delete its entry from the Hash Map tool
                    del self.cache[lru_node.key]
                    evicted_key = lru_node.key

            #now there's definitely room. Create the new node and add it to the front
            new_node = Node(key, value)

            #Add it to the front of the Timeline
            self.list.add_to_front(new_node)

            #save its address in the Dictionary
            self.cache[key] = new_node
        
        return evicted_key

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, size={len(self.list)})"
                
        
