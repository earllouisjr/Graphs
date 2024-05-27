from stack import Stack
from queue import Queue

class Graph:
    def __init__(self, V=None, E=None):
        raise NotImplementedError
    
    def bfs(self, v):
        tree = {}
        to_visit = Queue()
        to_visit.enqueue((None, v))
        while not to_visit.is_empty():
            prev, curr = to_visit.dequeue()
            if curr not in tree:
                tree[curr] = prev
                for n in self.neighbors(curr):
                    to_visit.enqueue((curr, n))
        return tree
    
    def dfs(self, v):
        tree = {}
        to_visit = Stack()
        to_visit.push((None, v))
        while not to_visit.is_empty():
            prev, curr = to_visit.pop()
            if curr not in tree:
                tree[curr] = prev
                for n in self.neighbors(curr):
                    to_visit.push((curr, n))
        return tree

    def connected(self, v1, v2):
        tree = self.bfs(v1)
        if v2 in tree:
            return True
        return False
    
    def shortest_path(self, v1, v2):
        tree = self.bfs(v1)
        if v2 not in tree:
            return float('inf'), None
        num_edges = 0
        curr_v = v2
        while curr_v is not v1:
            num_edges+=1
            curr_v = tree[curr_v]
        return num_edges, tree

    def has_cycle(self):
        visited = set()
        cycle_edges = []
        for vertex in self:
            if vertex not in visited:
                stack = Stack()
                stack.push((None, vertex))
                while not stack.is_empty():
                    prev, curr = stack.pop()
                    visited.add(curr)
                    for neighbor in self.neighbors(curr):
                        if neighbor in visited and neighbor != prev:
                            cycle_edges.append((neighbor, curr))
                            while stack.peek() != (neighbor, curr):
                                cycle_edges.append(stack.pop())
                            cycle_edges.reverse()
                            return True, cycle_edges
                        if neighbor not in visited:
                            stack.push((curr, neighbor))
        return False, None

class EdgeSetGraph(Graph):
    def __init__(self, V=(), E=()):
        self._V = set()
        self._E = set()
        if V: 
            for vertex in V: self.add_vertex(vertex)
        if E:
            for edge in E: self.add_edge(edge)
    
    def __iter__(self):
        return iter(self._V)

    def add_vertex(self, v):
        self._V.add(v)

    def add_edge(self, e):
        self._E.add(e)


    def neighbors(self, v):
        for i, j in self._E: 
            if i==v:
                yield j


class AdjacencySetGraph(Graph):
    def __init__(self, V=(), E=()):
        self._neighbors = {}
        if V:
            for vertex in V: self.add_vertex(vertex)
        if E:
            for edge in E: self.add_edge(edge)
    
    def __iter__(self):
        return iter(self._neighbors)

    def add_vertex(self, v):
        self._neighbors[v] = set()

    def add_edge(self, e):
        i, j = e
        self._neighbors[i].add(j)

    def neighbors(self, v):
        return iter(self._neighbors[v])

if __name__ == '__main__':
    V ={'A', 'B', 'C', 'D', 'E', 'F'}
    E ={('A', 'B'), ('A', 'C'),
        ('B', 'C'), ('B', 'D'),
        ('C', 'E'),
        ('D', 'F'),
        ('E', 'D'),
        ('F', 'E')}

    g = AdjacencySetGraph(V, E)
    print(g.connected('A', 'E'))
        # True
    print(g.bfs('A'))
        # {'A': None, 'B': 'A', 'C': 'A', 'D': 'B', 'E': 'C', 'F': 'D'}
    print(g.dfs('B'))
        # {'B': None, 'C': 'B', 'E': 'C', 'D': 'E', 'F': 'D'}
    print(g.has_cycle())
        # (True, [('D', 'F'), ('F', 'E'), ('E', 'D')])
    print(g.shortest_path('A', 'F'))
        # (3, [('A', 'B'), ('B', 'D'), ('D', 'F')])
