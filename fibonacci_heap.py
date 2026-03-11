#!/usr/bin/env python3
"""Fibonacci heap (simplified)."""
import sys, math
class FibNode:
    def __init__(self,k): self.k,self.deg,self.parent,self.child,self.mark=k,0,None,None,False; self.next=self.prev=self
class FibHeap:
    def __init__(self): self.min=None; self.n=0
    def insert(self,k):
        n=FibNode(k); self.n+=1
        if not self.min: self.min=n; return n
        n.next=self.min.next; n.prev=self.min; self.min.next.prev=n; self.min.next=n
        if k<self.min.k: self.min=n
        return n
    def find_min(self): return self.min.k if self.min else None
    def _roots(self):
        if not self.min: return []
        r,n=[],self.min
        while True:
            r.append(n); n=n.next
            if n==self.min: break
        return r
h=FibHeap()
for x in sys.argv[1:]: h.insert(int(x))
print(f"Min: {h.find_min()}, Size: {h.n}")
print(f"Roots: {[n.k for n in h._roots()]}")
