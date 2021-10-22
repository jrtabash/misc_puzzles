"""
Given a container, with a specified width, and a list of varying size 2D boxes,
calculate the linear feet, along the y-axis of the container needed to optimally
pack all the boxes.
"""

from puzzle_types import Final, Any, AnyCallback

# --------------------------------------------------------------------------------
# Geometric Helpers

class Point:
    """
    A 2D point, represented by (x, y)
    """

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

class Rectangle:
    """
    A 2D rectangle, represented by a point of origin, and x and y distances.
    """

    def __init__(self, origin: Point, xdist: int, ydist: int) -> None:
        self.origin: Point = origin
        self.xdist: int = xdist
        self.ydist: int = ydist
    
    def __str__(self) -> str:
        return f"[{self.origin} {self.xdist}x{self.ydist}]"
    
    def area(self) -> int:
        return self.xdist * self.ydist
    
    def xfeet(self) -> int:
        return self.origin.x + self.xdist
    
    def yfeet(self) -> int:
        return self.origin.y + self.ydist

# --------------------------------------------------------------------------------
# Node Classes

class Node:
    """
    Node represents a splitting of the container space, which would be one of 3 types;
    - Height := Splits space along the container length, y-axes
    - Width := Splits space along the container width, x-axis
    - Leaf := Area has a box
    """

    class Type:
        Height: Final = 'H' # Splits space along the y axis of the container, increases downwards
        Width: Final = 'W'  # Splits space across the x axis of the conainer, increases to the right
        Leaf: Final = 'L'   # A box

    def __init__(self, node_type: str, rectangle: Rectangle) -> None:
        self.node_type: str = node_type
        self.rectangle: Rectangle = rectangle

class Branch (Node):
    """
    A branch is a node that splits space eight by height or by width.
    """

    def __init__(self, branch_type: str, rectangle: Rectangle):
        super().__init__(branch_type, rectangle)
        self.left_child: Any = None
        self.right_child: Any = None
        
    def __str__(self) -> str:
        return f"[Branch: {self.node_type} {self.rectangle}]"
    
    def origin(self) -> Point:
        return self.rectangle.origin

    def xfeet(self) -> int:
        return self.rectangle.xfeet()

    def yfeet(self) -> int:
        return self.rectangle.yfeet()

class Leaf (Node):
    """
    A leaf is a node that represents a box
    """

    def __init__(self, rectangle: Rectangle) -> None:
        super().__init__(Node.Type.Leaf, rectangle)
    
    def __str__(self) -> str:
        return f"[Leaf: {self.rectangle}]"

# --------------------------------------------------------------------------------
# Box Class

class Box:
    """
    A 2D box.
    """

    def __init__(self, height: int, width: int) -> None:
        self.height: int = height
        self.width: int = width
    
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"

    def area(self) -> int:
        return self.height * self.width
    
    def make_nodes(self, origin: Point, verbose: bool = False) -> Any:
        """
        Will create
               [Branch: Y axis split]
              /
             [Branch: X axis split]
            /
           [Leaf: box]
        """
        rectangle = Rectangle(origin, self.width, self.height)
        hnode = Branch(Node.Type.Height, rectangle)
        wnode = Branch(Node.Type.Width, rectangle)
        wnode.left_child = Leaf(rectangle)
        hnode.left_child = wnode
        if verbose:
            print(f"***** make_nodes: hnode={hnode} wnode={wnode} rectangle={rectangle}")
        return hnode

# --------------------------------------------------------------------------------
# Tree Class and Helpers

class MaxDistCalc:
    """
    Functor to be used with Tree.walk_tree function.
    Will calculate the max distance (container depth/height needed to store the boxes.

    Requirements: Tree node distances must be pre-populated before this is used.
    """

    def __init__(self) -> None:
        self.distance = 0

    def __call__(self, node: Any) -> None:
        if isinstance(node, Branch) and node.node_type == Node.Type.Height:
            self.distance = max(self.distance, node.yfeet())

class PrintNode:
    """
    Functor to be used with Tree.walk_tree function.
    """

    def __call__(self, node: Any) -> None:
        if isinstance(node, Branch):
            print(f"{node} : left={node.left_child} right={node.right_child}")
        else:
            print(f"{node}\n")

class Tree:
    """
    Tree structure will hold the nodes that divide the space.
    Branch := Branch node that separates space either horzontall or vertically
    Leaf := Leaf node that holds a Box
    """

    def __init__(self, total_width: int, verbose: bool = False) -> None:
        self.root: Any = None
        self.total_width: int = total_width # Container width
        self.int_max_dist: int = 0 # Interim max distance
        self.verbose: bool = verbose

    def add_box(self, box: Box) -> None:
        self.log("----------")
        self.log(f"add_box: box={box} root={self.root} int_max_dist={self.int_max_dist}")
        if self.root is None:
            self.root = box.make_nodes(Point(0, 0), self.verbose)
            self.int_max_dist = self.root.yfeet()
        else:
            if not self.try_left(self.root, box):
                if not self.try_right(self.root, box):
                    self.new_height_split(self.root, box, True)

    def check_fits_right(self, box: Box, node: Branch) -> bool:
        new_width = node.xfeet() + box.width
        self.log(f"check_fits_right: box={box} node={node} new_width={new_width} max_width={self.total_width}")
        if new_width > self.total_width:
            return False
        return True
    
    def check_fits_below(self, box: Box, node: Branch) -> bool:
        self.log(f"check_fits_below: box={box} node={node} yfeet={node.yfeet()} int_max_dist={self.int_max_dist}")
        if node.origin().y >= self.int_max_dist:
            return False
        return node.xfeet() <= self.total_width

    def new_origin(self, node: Branch) -> Point:
        origin = None
        if (node.node_type == Node.Type.Height):
            origin = Point(node.origin().x, node.yfeet())
        else:
            assert(node.node_type == Node.Type.Width)
            origin = Point(node.xfeet(), node.origin().y)
        self.log(f"new_origin: node={node} origin={origin}")
        return origin

    def try_left(self, node: Branch, box: Box) -> bool:
        self.log(f"try_left: node={node} box={box}")
        # Left node assumed to always exist, because of use of function box.make_nodes
        left_node = node.left_child
        if left_node.right_child is None:
            if self.check_fits_right(box, node):
                left_node.right_child = box.make_nodes(self.new_origin(left_node), self.verbose)
                return True
        else:
            if self.try_left(left_node.right_child, box):
                return True
            if self.try_right(left_node.right_child, box):
                return True
        return False

    def try_right(self, node: Branch, box: Box) -> bool:
        self.log(f"try_right: node={node} box={box}")
        right_node = node.right_child
        if right_node is None:
            if self.check_fits_below(box, node):
                self.new_height_split(node, box, False)
                return True
        else:
            if self.try_left(right_node, box):
                return True
            if self.try_right(right_node, box):
                return True
        return False

    def new_height_split(self, node: Branch, box: Box, track_int: bool) -> None:
        self.log(f"new_height_split: node={node} box={box} track_int={track_int}")
        cur = node
        while cur.right_child is not None:
            cur = cur.right_child
        cur.right_child = box.make_nodes(self.new_origin(cur), self.verbose)
        if track_int:
            self.int_max_dist = cur.right_child.yfeet()

    def walk_tree(self, ftn: AnyCallback) -> None:
        def walk(node: Any):
            ftn(node)
            if isinstance(node, Branch):
                if node.left_child:
                    walk(node.left_child)
                if node.right_child:
                    walk(node.right_child)
        walk(self.root)

    def linear_feet(self) -> int:
        maxDist = MaxDistCalc()
        self.walk_tree(maxDist)
        return maxDist.distance
    
    def print_tree(self) -> None:
        self.walk_tree(PrintNode())
    
    def log(self, msg: str) -> None:
        if self.verbose:
            print(f"***** {msg}")

# --------------------------------------------------------------------------------
# Linear Feet Calculator Entry Point

def calc_linear_feet(boxes: list, container_width: int, print_tree: bool = False, verbose: bool = False) -> int:
    """
    Solve box packing problem:
    - Sort the boxes from largest area to smallest area
    - Create a empty tree, and add boxes to tree in sorted order
    - Walk tree to find max linear feet
    """

    boxes.sort(key=lambda box: box.area(), reverse=True)
    tree = Tree(container_width, verbose=verbose)
    for box in boxes:
        tree.add_box(box)
    if print_tree:
        tree.print_tree()
    return tree.linear_feet()

# --------------------------------------------------------------------------------
# Tests

def test() -> None:
    def test_case(container_width: int, boxes: list, expect_lin_feet: int) -> None:
        lin_feet = calc_linear_feet(boxes, container_width, verbose=False, print_tree=False)
        print(lin_feet)
        assert(lin_feet == expect_lin_feet)

    # Test 1
    # 
    # 1. 10x10
    # 2. 10x10
    # 3. 5x5
    # 4. 5x5
    # 
    # Container Width = 15, Optimal Linar Feet = 20
    test_case(container_width=15,
              boxes=[
                  Box(10, 10), Box(10, 10), Box(5, 5), Box(5, 5)
              ],
              expect_lin_feet=20)

    # Test 2
    # 
    # 1. 48x48
    # 2. 36x36
    # 3. 36x36
    # 
    # Container Width = 96, Optimal Linear Feet = 72
    test_case(container_width=96,
              boxes=[
                  Box(48, 48), Box(36, 36), Box(36, 36)
              ],
              expect_lin_feet=72)

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
    test_case(container_width=96,
              boxes=[
                  Box(48, 48),
                  Box(36, 36), Box(36, 36), Box(36, 36),
                  Box(24, 48), Box(24, 48)
              ],
              expect_lin_feet=108)

    # Test 4
    # 
    # 1. 48x48
    # 2. 48x48
    # 3. 48x48
    # 4. 36x36
    # 
    # Container Width = 96, Optimal Linear Feet = 96
    test_case(container_width=96,
              boxes=[
                  Box(48, 48), Box(48, 48), Box(48, 48),
                  Box(36, 36)
              ],
              expect_lin_feet=96)

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
    test_case(container_width=96,
              boxes=[
                  Box(48, 48), Box(48, 48), Box(48, 48),
                  Box(36, 36), Box(36, 36),
                  Box(24, 48), Box(24, 48), Box(24, 48)
              ],
              expect_lin_feet=144)

# --------------------------------------------------------------------------------
# Main

if __name__ == "__main__":
    test()
