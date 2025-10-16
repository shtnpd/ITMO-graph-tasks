from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class Graph(ABC):
    """
    Abstract base class for a graph. Stores:
      - vertices: number of vertices (0..n-1)
      - directed: whether the graph is directed
      - weighted: whether the graph is weighted
    """

    def __init__(self, vertices: int, directed: bool = False, weighted: bool = False):
        """Initialize basic graph properties and internal adjacency list.

        Args:
            vertices (int): number of vertices (>=0). Vertices are numbered 0..n-1.
            directed (bool, optional): True if the graph is directed. Defaults to False.
            weighted (bool, optional): True if the graph is weighted. Defaults to False.
        """
        if vertices < 0:
            raise ValueError("vertices must be non-negative")
        self.vertices = vertices
        self.directed = directed
        self.weighted = weighted
        self._adjacency_list: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(vertices)}

    def _check_vertex(self, v: int) -> None:
        """Helper method to verify vertex index validity.

        Args:
            v (int): Vertex index to validate.
        """
        if not (0 <= v < self.vertices):
            raise IndexError(f"vertex {v} is out of range [0, {self.vertices - 1}]")

    @abstractmethod
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """Abstract method for adding an edge (u -> v).

        Args:
            u (int): source vertex
            v (int): target vertex
            weight (float, optional): edge weight; should be ignored (and treated as 1.0)
                                      for unweighted graphs. Defaults to 1.0.

        Requirements:
            - Self-loops (u == v) are not allowed.
        """
        pass


    #   GRAPH REPRESENTATIONS

    def get_adjacency_list(self) -> Dict[int, List[Tuple[int, float]]]:
        """Returns the graph as an adjacency list
        """
        adj_list = {}

        for vertex, neighbors in self._adjacency_list.items():
            adj_list[vertex] = sorted(neighbors, key=lambda x: (x[0], x[1]))
            
        return adj_list


    def get_adjacency_matrix(self) -> List[List[float]]:
        """Returns the adjacency matrix of size n x n
        """
        n = self.vertices
        matrix = [[0.0] * n for _ in range(n)]
        
        for u in range(n):
            for v, weight in self._adjacency_list[u]:
                matrix[u][v] = weight if self.weighted else 1.0
                
        return matrix


    def get_incidence_matrix(self) -> List[List[int]]:
        """Returns the incidence matrix of size n x m (n = vertices, m = edges)
        """
        n = self.vertices
        edges = []
        seen_edges = set() # for undirected graphs

        for u in range(n):
            for v, _ in self._adjacency_list[u]:
                if self.directed:
                    edges.append((u, v))
                else:
                    edge = (min(u, v), max(u, v))
                    if edge not in seen_edges:
                        edges.append(edge)
                        seen_edges.add(edge)

        edges.sort()
        
        m = len(edges) 
        matrix = [[0] * m for _ in range(n)]

        for col, (u, v) in enumerate(edges):
            if self.directed:
                matrix[u][col] = -1
                matrix[v][col] = 1
            else:
                matrix[u][col] = 1
                matrix[v][col] = 1
                
        return matrix