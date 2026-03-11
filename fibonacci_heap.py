#!/usr/bin/env python3
"""Fibonacci Heap — amortized O(1) insert/decrease-key, O(log n) extract-min."""
import math

class FibNode:
    __slots__ = ('key', 'degree', 'parent', 'child', 'left', 'right', 'mark', 'value')
    def __init__(self, key, value=None):
        self.key, self.value = key, value
        self.degree = 0; self.parent = self.child = None
        self.left = self.right = self; self.mark = False

class FibonacciHeap:
    def __init__(self): self.min_node = None; self.n = 0
    
    def insert(self, key, value=None):
        node = FibNode(key, value)
        if self.min_node is None: self.min_node = node
        else:
            self._add_to_root(node)
            if key < self.min_node.key: self.min_node = node
        self.n += 1; return node
    
    def minimum(self): return self.min_node
    
    def extract_min(self):
        z = self.min_node
        if z is None: return None
        if z.child:
            children = self._get_siblings(z.child)
            for c in children: self._add_to_root(c); c.parent = None
        self._remove_from_list(z)
        if z.right == z: self.min_node = None
        else: self.min_node = z.right; self._consolidate()
        self.n -= 1; return z
    
    def decrease_key(self, node, new_key):
        if new_key > node.key: raise ValueError("New key greater")
        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            self._cut(node, parent); self._cascading_cut(parent)
        if node.key < self.min_node.key: self.min_node = node
    
    def _add_to_root(self, node):
        node.left = self.min_node; node.right = self.min_node.right
        self.min_node.right.left = node; self.min_node.right = node
    
    def _remove_from_list(self, node):
        node.left.right = node.right; node.right.left = node.left
    
    def _get_siblings(self, node):
        siblings = []; curr = node
        while True:
            siblings.append(curr); curr = curr.right
            if curr == node: break
        return siblings
    
    def _consolidate(self):
        max_degree = int(math.log2(self.n)) + 2 if self.n > 0 else 1
        A = [None] * (max_degree + 1)
        roots = self._get_siblings(self.min_node)
        for w in roots:
            x = w; d = x.degree
            while d < len(A) and A[d]:
                y = A[d]
                if x.key > y.key: x, y = y, x
                self._link(y, x); A[d] = None; d += 1
            if d >= len(A): A.extend([None] * (d - len(A) + 1))
            A[d] = x
        self.min_node = None
        for a in A:
            if a:
                a.left = a.right = a
                if self.min_node is None: self.min_node = a
                else:
                    self._add_to_root(a)
                    if a.key < self.min_node.key: self.min_node = a
    
    def _link(self, y, x):
        self._remove_from_list(y); y.parent = x
        if x.child is None: x.child = y; y.left = y.right = y
        else:
            y.left = x.child; y.right = x.child.right
            x.child.right.left = y; x.child.right = y
        x.degree += 1; y.mark = False
    
    def _cut(self, x, y):
        if x.right == x: y.child = None
        else:
            if y.child == x: y.child = x.right
            self._remove_from_list(x)
        y.degree -= 1; self._add_to_root(x); x.parent = None; x.mark = False
    
    def _cascading_cut(self, y):
        z = y.parent
        if z:
            if not y.mark: y.mark = True
            else: self._cut(y, z); self._cascading_cut(z)

if __name__ == "__main__":
    fh = FibonacciHeap()
    nodes = [fh.insert(k) for k in [7, 3, 17, 24, 1, 21, 13]]
    print(f"Min: {fh.minimum().key}, Size: {fh.n}")
    m = fh.extract_min(); print(f"Extracted: {m.key}")
    print(f"New min: {fh.minimum().key}")
    fh.decrease_key(nodes[2], 2)  # 17 -> 2
    print(f"After decrease: min={fh.minimum().key}")
