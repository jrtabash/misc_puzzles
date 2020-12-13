"""
Given a 2D matrix of 0s and 1s, where a group of connected 1s form an island,
count the number of islands.

For instance, the following matrix contains 2 islands.

  1 0 0 0 0
  1 1 0 1 1
  1 0 0 1 0
  0 0 0 1 0
  0 0 0 0 0

"""

from puzzle_types import IntMatrix, GraphMap, VertexSet, Final

ISLAND: Final = 1

def make_graph(world: IntMatrix) -> GraphMap:
    """
    Generate a graph of the world from the 2D matrix of 0s and 1s.
    """

    size: int = len(world)
    vertex_size: int = size * size
    graph: GraphMap = {v: [] for v in range(vertex_size)}

    def ij2vertex(i: int, j: int) -> int:
        return i * size + j

    def in_range(idx: int) -> bool:
        return 0 <= idx < size

    def check_and_add_edge(i: int, j: int, dest_i: int, dest_j: int) -> None:
        if world[i][j] == ISLAND:
            if (i == dest_i or in_range(dest_i)) and (j == dest_j or in_range(dest_j)):
                if world[dest_i][dest_j] == ISLAND:
                    graph[ij2vertex(i, j)].append(ij2vertex(dest_i, dest_j))

    for i in range(size):
        for j in range(size):
            check_and_add_edge(i, j, i, j)
            check_and_add_edge(i, j, i, j - 1)
            check_and_add_edge(i, j, i, j + 1)

            check_and_add_edge(i, j, i - 1, j)
            check_and_add_edge(i, j, i - 1, j - 1)
            check_and_add_edge(i, j, i - 1, j + 1)

            check_and_add_edge(i, j, i + 1, j)
            check_and_add_edge(i, j, i + 1, j - 1)
            check_and_add_edge(i, j, i + 1, j + 1)

    return graph

def count_islands(graph: GraphMap) -> int:
    """
    Calculate the number of islands in the graph, where connected
    nodes/vertices form an island.
    """

    count: int = 0

    remaining: VertexSet = set(graph.keys())
    while len(remaining) > 0:
        vertex: int = remaining.pop()
        if len(graph[vertex]) > 0:
            remaining -= find_connected(graph, vertex)
            count += 1

    return count

def find_connected(graph: GraphMap, from_vertex: int) -> VertexSet:
    """
    Find all connected vertices starting from given vertex.
    """

    visited: VertexSet = set()
    to_visit: VertexSet = set()

    def mark_and_collect(src_vertex):
        visited.add(src_vertex)
        for vertex in graph[src_vertex]:
            to_visit.add(vertex)

    mark_and_collect(from_vertex)

    while len(to_visit) > 0:
        dest_vertex: int = to_visit.pop()
        if dest_vertex not in visited:
            mark_and_collect(dest_vertex)

    return visited

def test_islands() -> None:
    """
    Test number of islands.
    """

    def test_case(name: str, actual_count: int, world_map: IntMatrix) -> None:
        count = count_islands(make_graph(world_map))
        print(f"{name}: count={count} actual={actual_count}")

    test_case("test1", 1,
              [[1, 0],
               [1, 1]])

    test_case("test2", 2,
              [[1, 0, 0, 0],
               [1, 1, 0, 1],
               [1, 0, 0, 1],
               [0, 0, 1, 1]])

    test_case("test3", 3,
              [[1, 0, 0, 0, 0],
               [1, 1, 0, 1, 1],
               [1, 0, 0, 1, 0],
               [0, 0, 0, 1, 0],
               [1, 1, 0, 0, 0]])

    test_case("test4", 4,
              [[0, 1, 0, 1, 0],
               [1, 1, 0, 1, 1],
               [0, 1, 0, 0, 1],
               [0, 0, 0, 0, 0],
               [0, 1, 0, 0, 1]])

if __name__ == "__main__":
    test_islands()
