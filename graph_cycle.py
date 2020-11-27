"""
Check if a directed graph contains a cycle. Given a list
of vertices V, and list of Edges E, build a Grpah instance
and use its has_cycle function to check if it contains a
cycle.
"""

import typing

InputVertices = typing.Sequence[int]
InputEdges = typing.Sequence[typing.Tuple[int, int]]

GraphVertices = typing.Mapping[int, typing.MutableSequence[int]]
VertexSet = typing.MutableSet[int]

class Graph:
    """
    This class represents a graph (V, E) with V vertices and E edges.
    """

    def __init__(self, vertices: InputVertices, edges: InputEdges) -> None:
        self.vertices: GraphVertices = {v: [] for v in vertices}
        for edge in edges:
            self.vertices[edge[0]].append(edge[1])

    def has_cycle(self) -> bool:
        """
        Check if graph has a cycle.
        """

        top_vertices: VertexSet = set(self.vertices.keys())
        while len(top_vertices) > 0:
            vertex: int = top_vertices.pop()
            if self.detect_cycle(vertex, top_vertices):
                return True
        return False

    def detect_cycle(self, from_vertex: int, top_vertices: VertexSet) -> bool:
        """
        Starting from given vertex, walk the edges, tracking visited vertices in the process.
        Function returns true if it detects a cycle, false otherwise.
        The function removes encountered vertices from the top_vertices set.
        """

        visited: VertexSet = set()
        to_visit: VertexSet = set()

        def mark_and_collect(src_vertex):
            visited.add(src_vertex)
            for vertex in self.vertices[src_vertex]:
                if vertex in top_vertices:
                    top_vertices.remove(vertex)
                to_visit.add(vertex)

        mark_and_collect(from_vertex)

        while len(to_visit) > 0:
            dest_vertex: int = to_visit.pop()
            if dest_vertex in visited:
                return True
            mark_and_collect(dest_vertex)

        return False

def test_cycle() -> None:
    """
    Test if graphs have cycles.
    """

    def test_graph(name: str, graph: Graph, cycle_flag: str) -> None:
        if graph.has_cycle():
            print(f"{name}: Has Cycle [{cycle_flag}]")
        else:
            print(f"{name}: No Cycles [{cycle_flag}]")

    test_graph("graph1",
               Graph([1, 2, 3],
                     [(1, 2), (1, 3), (2, 3)]),
               "N")
    test_graph("graph2",
               Graph([1, 2, 3, 4, 5],
                     [(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5)]),
               "N")
    test_graph("graph3",
               Graph([1, 2, 3, 4],
                     [(1, 2), (1, 3), (2, 3), (4, 1), (4, 4)]),
               "C")
    test_graph("graph4",
               Graph([1, 2, 3, 4, 5],
                     [(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 1), (4, 5)]),
               "C")
    test_graph("graph5",
               Graph([1, 2, 3, 4, 5, 6],
                     [(1, 2), (1, 3), (2, 3), (3, 5), (4, 1), (5, 4)]),
               "C")

if __name__ == "__main__":
    test_cycle()
