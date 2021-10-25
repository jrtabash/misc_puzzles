"""
Given a container, with a specified width, and a list of varying size 2D boxes,
calculate the linear distance, along the y-axis of the container needed to pack
all the boxes.
"""

import sys
import numpy as np
from puzzle_types import Any, Optional, Tuple, Final

POINT: Final = 0
BOX: Final = 1

# --------------------------------------------------------------------------------
# Point

Point = Tuple[int, int, int]

def make_point(h: int, w: int) -> Point:
    return (POINT, h, w)
    
def is_point(pt: Any) -> bool:
    return isinstance(pt, tuple) and pt[0] == POINT
    
def point_height(pt: Point) -> int:
    return pt[1]

def point_width(pt: Point) -> int:
    return pt[2]

def prt_point(pt: Point):
    print(f"({point_height(pt)},{point_width(pt)})")

# --------------------------------------------------------------------------------
# Box

Box = Tuple[int, int, int, int]

def make_box(tag: int, h: int, w: int) -> Box:
    return (BOX, h, w, tag)

def is_box(box: Any) -> bool:
    return isinstance(box, tuple) and box[0] == BOX

def box_height(box: Box) -> int:
    return box[1]

def box_width(box: Box) -> int:
    return box[2]

def box_tag(box: Box) -> int:
    return box[3]

def box_area(box: Box) -> int:
    return box_height(box) * box_width(box)

def prt_box(box: Box):
    print(f"{box_tag(box)}:{box_height(box)}x{box_width(box)}")

# --------------------------------------------------------------------------------
# Container

Container = np.ndarray

def make_container(h: int, w: int) -> Container:
    return np.zeros((h, w), dtype=np.int16)

def is_container(container: Any) -> bool:
    return isinstance(container, np.ndarray)

def container_height(container: Container) -> int:
    return container.shape[0]

def container_width(container: Container) -> int:
    return container.shape[1]

def container_max_dist(container: Container) -> int:
    dist = 0
    for row in container:
        if np.sum(row) == 0:
            break
        dist += 1
    return dist

def prt_container(container: Container, empty: bool = True):
    for row in container:
        if not empty and np.all(row == 0):
            break
        for cell in row:
            print(cell, end="")
        print("")

# --------------------------------------------------------------------------------
# Algorithm

def find_add_point(container: Container, box: Box) -> Optional[Point]:
    assert(is_container(container))
    assert(is_box(box))
    for h in range(container_height(container)):
        for w in range(container_width(container)):
            if container[h, w] == 0:
                if (w + box_width(box)) <= container_width(container):
                    if np.all(container[h:h+box_height(box), w:w+box_width(box)] == 0):
                        return make_point(h, w)
    return None

def add_box(container: Container, box: Box):
    sp = find_add_point(container, box)
    assert(sp is not None)
    ep = make_point(point_height(sp) + box_height(box), point_width(sp) + box_width(box))
    container[point_height(sp):point_height(ep), point_width(sp):point_width(ep)] = box_tag(box)

def calc_dist(cw: int, boxes: list, trace: bool = False) -> int:
    def try_calc(reverse: bool):
        boxes.sort(key=lambda b: box_area(b), reverse=reverse)

        if trace:
            for box in boxes:
                prt_box(box)

        ch = box_height(boxes[0]) * len(boxes)
        container = make_container(ch, cw)
        for box in boxes:
            add_box(container, box)

        if trace:
            prt_container(container, empty=False)

        return container_max_dist(container)

    return min(try_calc(True), try_calc(False))

# --------------------------------------------------------------------------------
# Tests

def run_test(which="all", trace=False):
    def test_case(name, case):
        global NEXT_ID
        NEXT_ID = 0
        def next_id():
            global NEXT_ID
            NEXT_ID += 1
            return NEXT_ID

        dist = calc_dist(
                cw=case["container_width"],
                boxes=[make_box(next_id(), h, w) for h, w in case["boxes"]],
                trace=trace)

        check = case["check"]
        success = dist == check
        print(f"{name}\t{dist}\t{check}\t{success}")

    tests = {
        # Test 0
        # 
        # 1. 2x5
        # 2. 4x3
        # 3. 4x2
        # 4. 2x3
        #
        # Container Width = 10, Optimal Linear Feet = 4
        "test0": dict(container_width=10,
                      boxes=[(2, 5), (4, 3), (4, 2), (2, 3)],
                      check=4),

        # Test 1
        # 
        # 1. 10x10
        # 2. 10x10
        # 3. 5x5
        # 4. 5x5
        # 
        # Container Width = 15, Optimal Linear Feet = 20
        "test1": dict(container_width=15,
                      boxes=[
                          (10, 10), (10, 10), (5, 5), (5, 5)
                      ],
                      check=20),

        # Test 2
        # 
        # 1. 48x48
        # 2. 36x36
        # 3. 36x36
        # 
        # Container Width = 96, Optimal Linear Feet = 72
        "test2": dict(container_width=96,
                      boxes=[
                          (48, 48), (36, 36), (36, 36)
                      ],
                      check=72),

        # Test 3
        # 
        # 1. 48x48
        # 2. 36x36
        # 3. 36x36
        # 4. 36x36
        # 5. 24x48
        # 6. 24x48
        # 
        # Container Width = 96, Optimal Linear Feet = 108
        "test3": dict(container_width=96,
                      boxes=[
                          (48, 48),
                          (36, 36), (36, 36), (36, 36),
                          (24, 48), (24, 48)
                      ],
                      check=108),

        # Test 3.1
        # 
        # 1. 8x8
        # 2. 6x6
        # 3. 6x6
        # 4. 6x6
        # 5. 4x8
        # 6. 4x8
        # 
        # Container Width = 16, Optimal Linear Feet = 18
        "test3.1": dict(container_width=16,
                        boxes=[
                            (8, 8),
                            (6, 6), (6, 6), (6, 6),
                            (4, 8), (4, 8)
                        ],
                        check=18),

        # Test 3.5
        # 
        # 1. 12x12
        # 2. 8x8
        # 3. 8x8
        # 4. 8x8
        # 5. 6x12
        # 6. 6x12
        # 
        # Container Width = 24, Optimal Linear Feet = 20
        "test3.5": dict(container_width=24,
                        boxes=[
                            (12, 12),
                            (8, 8), (8, 8), (8, 8),
                            (6, 12), (6, 12)
                        ],
                        check=20),

        # Test 4
        # 
        # 1. 48x48
        # 2. 48x48
        # 3. 48x48
        # 4. 36x36
        # 
        # Container Width = 96, Optimal Linear Feet = 96
        "test4": dict(container_width=96,
                      boxes=[
                          (48, 48), (48, 48), (48, 48),
                          (36, 36)
                      ],
                      check=96),

        # Test 5
        # 
        # 1. 48x48
        # 2. 48x48
        # 3. 48x48
        # 4. 36x36
        # 5. 36x36
        # 6. 24x48
        # 7. 24x48
        # 8. 24x48
        # 
        # Container Width = 96, Optimal Linear Feet = 144
        "test5": dict(container_width=96,
                      boxes=[
                          (48, 48), (48, 48), (48, 48),
                          (36, 36), (36, 36),
                          (24, 48), (24, 48), (24, 48)
                      ],
                      check=144),

        # Test 6
        #
        # 1. 20x10
        # 2. 10x10
        # 3. 10x10
        # 4. 10x10
        # 5. 10x10
        #
        # Container Width = 30, Optimal Linear Feet = 20
        "test6": dict(container_width=30,
                      boxes=[
                          (20, 10),
                          (10, 10), (10, 10), (10, 10), (10, 10)
                      ],
                      check=20),

        # Test 6.5
        #
        # 1. 20x10
        # 2. 10x10
        # 3. 10x10
        #
        # Container Width = 30, Optimal Linear Feet = 20
        "test6.5": dict(container_width=30,
                        boxes=[
                            (20, 10),
                            (10, 10), (10, 10)
                        ],
                        check=20),

        # Test 7
        #
        # 1. 20x10
        # 2. 10x10
        # 3. 10x10
        # 4. 10x10
        # 5. 10x10
        #
        # Container Width = 20, Optimal Linear Feet = 30
        "test7": dict(container_width=20,
                      boxes=[
                          (20, 10),
                          (10, 10), (10, 10), (10, 10), (10, 10)
                      ],
                      check=30),

        # Test 8
        #
        # 1. 13x10
        # 2. 10x10
        # 3. 10x10
        # 4. 10x10
        # 5. 10x10
        #
        # Container Width = 30, Optimal Linear Feet = 20
        "test8": dict(container_width=30,
                      boxes=[
                          (13, 10),
                          (10, 10), (10, 10), (10, 10), (10, 10)
                      ],
                      check=20),

        # Test 9
        #
        # 1. 13x10
        # 2. 10x10
        # 3. 10x10
        # 4. 10x10
        # 5. 10x10
        #
        # Container Width = 20, Optimal Linear Feet = 30
        "test9": dict(container_width=20,
                      boxes=[
                          (13, 10),
                          (10, 10), (10, 10), (10, 10), (10, 10)
                      ],
                      check=30),

        # Test 10
        #
        # 1. 13x10
        # 2. 5x10
        # 3. 5x10
        # 4. 5x10
        # 5. 5x10
        #
        # Container Width = 20, Optimal Linear Feet = 18
        "test10": dict(container_width=20,
                       boxes=[
                           (13, 10),
                           (5, 10), (5, 10), (5, 10), (5, 10)
                       ],
                       check=18),

        # Test 11
        # 
        # 1. 48x48
        # 2. 48x48
        # 3. 48x48
        # 
        # Container Width = 96, Optimal Linear Feet = 96
        "test11": dict(container_width=96,
                       boxes=[
                           (48, 48), (48, 48), (48, 48)
                       ],
                       check=96),

        # Test 12
        # 
        # 1. 48x48
        # 2. 48x48
        # 3. 48x48
        # 4. 48x48
        # 
        # Container Width = 96, Optimal Linear Feet = 96
        "test12": dict(container_width=96,
                       boxes=[
                           (48, 48), (48, 48), (48, 48), (48, 48)
                       ],
                       check=96),

        # Test 13
        # 
        # 1. 48x48
        # 2. 48x48
        # 3. 48x48
        # 4. 48x48
        # 5. 48x48
        # 
        # Container Width = 96, Optimal Linear Feet = 144
        "test13": dict(container_width=96,
                       boxes=[
                           (48, 48), (48, 48), (48, 48), (48, 48), 
                           (48, 48)
                       ],
                       check=144),

        # Test 14
        # 
        # 1. 48x48
        # 2. 48x48
        # 3. 48x48
        # 4. 48x48
        # 5. 48x48
        # 6. 48x48
        # 7. 48x48
        # 8. 48x48
        # 9. 48x48
        # 
        # Container Width = 96, Optimal Linear Feet = 240
        "test14": dict(container_width=96,
                       boxes=[
                           (48, 48), (48, 48), (48, 48), (48, 48), 
                           (48, 48), (48, 48), (48, 48), (48, 48), 
                           (48, 48)
                       ],
                       check=240)
    }

    print("Test\tDist\tCheck\tSuccess")
    if which == "all":
        for name, case in tests.items():
            test_case(name, case)
    else:
        test_case(which, tests[which])

# --------------------------------------------------------------------------------
# Main

def main():
    # Usage:
    #   python3 box_packing.py [<test_name>] [trace]

    which = "all"
    trace = False
    if len(sys.argv) >= 2:
        which = sys.argv[1]
    if len(sys.argv) >= 3:
        trace = sys.argv[2] == "trace"
    run_test(which, trace)

if __name__ == "__main__":
    main()
