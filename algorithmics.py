from typing import List, Dict
from graph_abc import Graph


class GraphAlgorithms:
    """
    A collection of algorithms operating on Graph objects.
    This implementation utilizes all available graph representations:
      - get_adjacency_list() - primary representation used in all algorithms
      - get_adjacency_matrix() - used for optimized neighbor lookups in BFS/DFS
      - get_incidence_matrix() - used for optimized edge detection in component analysis
    """

    @staticmethod
    def bfs(graph: Graph, start: int) -> List[int]:
        """
        Breadth-First Search starting from vertex start
        """
        if not 0 <= start < graph.vertices:
            raise IndexError(f"vertex {start} is out of range [0, {graph.vertices - 1}]")
        
        from collections import deque
        
        adj_list = graph.get_adjacency_list()
        adj_matrix = graph.get_adjacency_matrix()
        
        visited = [False] * graph.vertices
        result = []

        queue = deque([start])
        visited[start] = True

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for v in range(graph.vertices):
                if adj_matrix[vertex][v] > 0 and not visited[v]:
                    visited[v] = True
                    queue.append(v)
        
        return result

    @staticmethod
    def dfs(graph: Graph, start: int) -> List[int]:
        """
        Depth-First Search starting from vertex start
        """
        if not 0 <= start < graph.vertices:
            raise IndexError(f"vertex {start} is out of range [0, {graph.vertices - 1}]")

        adj_matrix = graph.get_adjacency_matrix()

        visited = [False] * graph.vertices
        result = []
        
        def dfs_recursive(vertex: int):
            visited[vertex] = True
            result.append(vertex)

            for v in range(graph.vertices):
                if adj_matrix[vertex][v] > 0 and not visited[v]:
                    dfs_recursive(v)

        dfs_recursive(start)
        return result

    @staticmethod
    def connected_components(graph: Graph) -> List[List[int]]:
        """
        Finds connected components in the graph
        """
        adj = graph.get_adjacency_list()
        inc_matrix = graph.get_incidence_matrix()

        visited = [False] * graph.vertices
        components = []
        
        def dfs_component(vertex: int, current_component: List[int]):
            visited[vertex] = True
            current_component.append(vertex)

            for edge_idx in range(len(inc_matrix[0])):
                if graph.directed:
                    if inc_matrix[vertex][edge_idx] == -1:
                        for v in range(graph.vertices):
                            if inc_matrix[v][edge_idx] == 1 and not visited[v]:
                                dfs_component(v, current_component)
                    elif inc_matrix[vertex][edge_idx] == 1:
                        for v in range(graph.vertices):
                            if inc_matrix[v][edge_idx] == -1 and not visited[v]:
                                dfs_component(v, current_component)
                else:
                    if inc_matrix[vertex][edge_idx] == 1:
                        for v in range(graph.vertices):
                            if v != vertex and inc_matrix[v][edge_idx] == 1 and not visited[v]:
                                dfs_component(v, current_component)
        
        for vertex in range(graph.vertices):
            if not visited[vertex]:
                current_component = []
                dfs_component(vertex, current_component)
                current_component.sort()
                components.append(current_component)
        
        components.sort(key=lambda x: x[0])
        
        return components

    @staticmethod
    def components_with_stats(graph: Graph) -> List[Dict[str, object]]:
        """
        Returns statistics for each connected component
        """
        components = GraphAlgorithms.connected_components(graph)
        adj_matrix = graph.get_adjacency_matrix()
        inc_matrix = graph.get_incidence_matrix()

        vertex_to_component = {}
        for i, component in enumerate(components):
            for vertex in component:
                vertex_to_component[vertex] = i

        stats = []
        for component in components:
            node_count = len(component)
            smallest_vertex = component[0]
            edge_count = 0
            
            if graph.directed:
                for u in component:
                    for v in component:
                        if adj_matrix[u][v] > 0:
                            edge_count += 1
            else:
                for u in component:
                    for v in component:
                        if u < v and adj_matrix[u][v] > 0:
                            edge_count += 1
            
            edge_set = set()
            for edge_idx in range(len(inc_matrix[0])):
                edge_vertices = []
                for v in component:
                    if inc_matrix[v][edge_idx] != 0:
                        edge_vertices.append(v)
                
                if len(edge_vertices) == 2:
                    u, v = edge_vertices
                    if not graph.directed:
                        u, v = min(u, v), max(u, v)
                    edge_set.add((u, v))

            assert edge_count == len(edge_set), "Edge count"
            
            stats.append({
                "vertices": component,
                "node_count": node_count,
                "edge_count": edge_count,
                "smallest_vertex": smallest_vertex
            })
        
        stats.sort(key=lambda x: (-x["node_count"], -x["edge_count"], x["smallest_vertex"]))
        
        return stats
