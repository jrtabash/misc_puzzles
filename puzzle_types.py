"""
Module containing common typing components used by puzzle solutions
in the misc_puzzles repo.
"""

import typing
from typing import Final

# -------------------------
# Integer Misc

IntArray = typing.MutableSequence[int]
IntMatrix = typing.Sequence[IntArray]

IntMap = typing.MutableMapping[int, int]
IntSet = typing.MutableSet[int]

IntPair = typing.Tuple[int, int]
OptIntPair = typing.Optional[IntPair]

# -------------------------
# Functions / Generators

NextIndexFtn = typing.Callable[[int], int]
IntGenerator = typing.Generator[int, None, None]

# -------------------------
# Grid / Board

Grid = IntMatrix
Board = IntMatrix

# -------------------------
# Graph

VertexArray = IntArray
VertexSet = IntSet

Edge = typing.Tuple[int, int]
EdgeArray = typing.MutableSequence[Edge]

GraphMap = typing.MutableMapping[int, typing.MutableSequence[int]]

BoolVerticesPair = typing.Tuple[bool, VertexSet]
