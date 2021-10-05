
from node import Node
from itertools import combinations


def x_product(n1: Node, n2: Node):
    return n1.x * n2.y - n2.x * n1.y


def line_3Node(p1: Node, p2: Node, p3: Node):
    return round(x_product(p2 - p1, p3 - p1), 4) == 0


class Line:

    def __init__(self, node1: Node, node2: Node) -> None:
        self.n1 = node1
        self.n2 = node2

        # keep n1 be the one with smaller x
        if self.n2.x < self.n1.x:
            self.n1, self.n2 = self.n2, self.n1

        # legacy slop finding method

        # self.slope = None
        # self.intercept = None

        # # if same x then run is 0 error, so no intercept or slope
        # if self.n1.x != self.n2.x:
        #     # y2 - y1 / x2 - x1
        #     self.slope = (self.n2.y - self.n1.y)/(self.n1.x - self.n2.x)

        #     # (x2 * y1 - x1 * y2) / (x2 - x1)
        #     self.intercept = (self.n2.x * self.n1.y -
        #                       self.n1.x * self.n2.y)/(self.n2.x - self.n1.x)

    def __eq__(self, o) -> bool:
        return isinstance(o, Line) and (
            self.n1 == o.n1 and self.n2 == o.n2
            or self.n2 == o.n1 and self.n1 == o.n2)

    def __hash__(self) -> int:
        return self.n1.__hash__() + self.n2.__hash__()

    def __repr__(self) -> str:
        return f'Line[{self.n1},{self.n2}]'

    # is_intersection_on_line_Lines

    def bound(self, node: Node):
        '''
        check if a Node is bounded by such line 
        note: the Node should already be checked to be on the line. 
            this check if it is within its bounding limit
        '''
        x_bound = sorted([self.n1.x, self.n2.x])
        y_bound = sorted([self.n1.y, self.n2.y])

        return x_bound[0] <= node.x <= x_bound[1] and y_bound[0] <= node.y <= y_bound[1]

    def lns_on_same_line(self, seg):
        """
        :param seg: another Line
        :return: bool
        """
        return line_3Node(self.n1, self.n2, seg.n1) and line_3Node(self.n1, self.n2, seg.n2)

    def same_line_intersects(self, seg):
        """
        use it only when 2 Lines are on e same line
        :param seg: another Line
        :return: bool
        """
        return (min(self.n1.x, self.n2.x) <= max(seg.n1.x, seg.n2.x)) and \
            (max(self.n1.x, self.n2.x) >= min(seg.n1.x, seg.n2.x)) and \
            (min(self.n1.y, self.n2.y) <= max(seg.n1.y, seg.n2.y)) and \
            (max(self.n1.y, self.n2.y) >= min(seg.n1.y, seg.n2.y))

    def overlaps(self, seg):
        """
        use it only when 2 Lines are on the same line and intersect
        :param seg: another Line
        :return: set(): intersection Nodes.
                 empty when not overlap
                 len = 1 when overlaps at the end
                 len = 2 when overlaps a range
        """
        if self == seg:
            return {self.n1, self.n2}
        node_list = [self.n1, self.n2, seg.n1, seg.n2]
        node_set = set(node_list)     # set literal
        far_ends = set()
        max_dist = 0
        for pair in combinations(node_set, 2):
            dist = pair[0].dist(pair[1])
            if dist >= max_dist:
                max_dist = dist
                far_ends = {pair[0], pair[1]}

        for node in far_ends:
            node_list.remove(node)
        return set(node_list)

    def straddle(self, seg):
        """
        :param seg: another Line
        :return if the other Line cross the corresponding line of self, return true.
        """
        v = self.n2 - self.n1
        v1 = seg.n1 - self.n1
        v2 = seg.n2 - self.n1
        # == 0: when one end of a Line is on the other Line
        return x_product(v1, v) * x_product(v2, v) <= 0
        #     return True
        # else:
        #     return False

    def is_intersected(self, seg):
        """
        use it only when Lines are not on the same line
        :param seg: another Line
        """
        if self.straddle(seg) and seg.straddle(self):
            return True
        else:
            return False

    def contains_node(self, Node):
        """
        judge whether a Node is on the Line
        :param Node: another Node
        :return: bool
        """
        v1 = Node - self.n1
        v2 = Node - self.n2
        if x_product(v1, v2) != 0:  # Node is not on the line of self
            return False

        x_min = min(self.n1.x, self.n2.x)
        x_max = max(self.n1.x, self.n2.x)
        if Node.x < x_min or Node.x > x_max:
            return False
        y_min = min(self.n1.y, self.n2.y)
        y_max = max(self.n1.y, self.n2.y)
        if Node.y < y_min or Node.y > y_max:
            return False
        return True


def intersect(l1: Line, l2: Line):
    """Returns a Node at which two lines intersect"""
    x1, y1 = l1.n1.x, l1.n1.y
    x2, y2 = l1.n2.x, l1.n2.y

    x3, y3 = l2.n1.x, l2.n1.y
    x4, y4 = l2.n2.x, l2.n2.y

    xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
    xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    xcoor = xnum / xden

    ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    ycoor = ynum / yden

    return Node(xcoor, ycoor)


