#!/usr/bin/env python3
import sys
import shlex
import re
from sys import stderr
from itertools import combinations

# YOUR CODE GOES HERE

RM = 'rm'
ADD = 'add'
MOD = 'mod'
GG = 'gg'
COMMAND = [RM, ADD, MOD, GG]



class Node:
    def __init__(self, x, y) -> None:
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f'Node({self.x:.4f},{self.y:.4f})'

    # def __eq__(self, other):
    #     return isinstance(other, Node) and (self.x, self.y) == (other.x, other.y)

    def __eq__(self, other) -> bool:
        return isinstance(other, Node) and round(self.x, 4) == round(other.x, 4) and round(self.y, 4) == round(other.y, 4)

    def __hash__(self) -> int:
        return hash('x' + str(round(self.x, 4)) + 'y' + str(round(self.y, 4)))

    def __sub__(self, other):
        return Node(self.x - other.x, self.y - other.y)

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def dist_sqr(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2



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


class Street:
    '''Street class keep track of all entered streets'''

    def __init__(self) -> None:
        self.street_db: dict = dict()

    def add(self, street_name: str, coordinates: list) -> None:
        if street_name not in self.street_db:
            self.street_db[street_name] = coordinates
        else:
            print(f'Error: Street.add(): {street_name} already exists', file=stderr)

    def modify(self, street_name: str, coordinates: list):
        if street_name in self.street_db:
            self.street_db[street_name] = coordinates
        else:
            print(f'Error: Street.modify(): {street_name} does not exists', file=stderr)

    def remove(self, street_name):
        if street_name in self.street_db:
            del self.street_db[street_name]
        else:
            print(f'Error: Street.remove(): {street_name} does not exists', file=stderr)

    def to_line(self):
        street_lns = {}
        for street, coordinates in self.street_db.items():
            # DEBUG gg recieved line segments
            # print(street, coordinates)
            # lns = []
            lns = set()
            for a, b in zip(coordinates[:-1], coordinates[1:]):
                lns.add(Line(a, b))

            street_lns[street] = lns
        return street_lns

    def generate_graph(self):
        graph = Graph(self.street_db)
        graph.generate_graph()


def get(l, idx):
    try:
        return l[idx]
    except IndexError:
        return None


class InputContent:

    def __init__(self) -> None:
        self.status, self.cmd, self.street_name, self.coordinates = [None] * 4


def process_input(line) -> InputContent:
    '''Process the command based on line
    return
    status: wether this has been parsed successfully
    command: a valid command,
    street_name: a street name,
    coordinates: a list of coordiantes;
    '''
    r = InputContent()

    sp = shlex.split(line)
    cmd, street_name, cord = get(sp, 0), get(sp, 1), ' '.join(sp[2:])
    # print(f'Command:{cmd}\nStreet:{street_name}\nCoordinates:{cord}\n')

    r.status = True

    # if command not valid then return
    if cmd not in COMMAND:
        print(
            f'Error: Your command "{cmd}" is not one of {COMMAND}, try again.', file=stderr)
        r.status = False
        return r

    r.cmd = cmd  # cmd must be valid here, put it in.

    # if the command is gg, then no need to parse street name or coordinates, nor any need to reject it
    if cmd == GG:
        # print(street_name, cord)
        if street_name is not None or cord != '':
            print(
                f'Error "gg" command cannot have parameters, try again.', file=stderr)
            r.status = False
        return r

    # if street name does not exist;
    street_name = street_name.strip().lower()
    if not street_name or street_name == '':
        print(
            f'Error: Your street_name: "{street_name}" for {cmd} is invalid, try again.', file=stderr)
        r.status = False
        return r
    elif not all(chre.isalpha() or chre.isspace() for chre in street_name):
        print('Error: Street name must contain only letters and spaces.', file=stderr)
        r.status = False
        return r


    # street name must be valid here
    r.street_name = street_name

    # rm does not need coordiates, exit here
    if cmd == RM:
        if cord != '':
            print('Error rm cannot have more than 2 arguments', file=stderr)
            r.status = False
        return r

    if not cord:
        print(
            f'Error: Your coordinates: "{cord}" for {cmd} is invalid, try again.', file=stderr)
        r.status = False
        return r

    # processing coordinates
    li = []
    for match in re.findall(r'(?<=\().*?(?=\))', cord):
        a, b = map(float, match.split(','))
        # li.append([a, b]) # return raw

        # return a list of Nodes
        li.append(Node(a, b))

    if cmd == ADD:
        if len(li) <= 1:
            print(f'Error: for adding {r.__dict__}, {li}, {cord} you cannot have only 1 coordinate. ', file=sys.stderr)
            r.status = False
            return r

    r.coordinates = li
    return r



class Graph:
    def __init__(self):
        # dict(3-level) (key: str(street), val: {key: seg-ref, val: {key: Node, val: int [point-ref]}} )
        self.vertices = {}
        self.edges = set()     # set of Lines
        # self.edges = []     # list of Lines

    # for test only
    def output_street_vertices(self):
        print("V = {")
        for street_points in self.vertices.items():
            print("====== street name: " + street_points[0] + " ======")
            for seg_points in street_points[1].items():
                print("    == seg ref: " + str(seg_points[0]) + " ==")
                for point_ref_pair in seg_points[1].items():
                    print(
                        "        " + str(point_ref_pair[1]) + ": " + (point_ref_pair[0]))
        print("}")

    def gen_output_vertices_dict(self):
        vertices_dict = {}
        for sub1_dict in self.vertices.values():
            for sub2_dict in sub1_dict.values():
                for point in sub2_dict:
                    vertices_dict[point] = sub2_dict[point]  # reference_number
        return vertices_dict

    def output(self):   # or __str__, __repr__ ?
        print("V = {")
        output_vertices_dict = self.gen_output_vertices_dict()
        for point in output_vertices_dict:
            print(f'  {str(output_vertices_dict[point])}: ({point.x:.2f}, {point.y:.2f})')
        print("}")

        # for test only
        # print("E = {")
        # for item in self.edges:
        #     print("  <" + str(item.n1) + "," + str(item.n2) + ">")
        # print("}")

        print("E = {")
        edges_list = list(self.edges)
        if len(edges_list) != 0:
            for item in edges_list[:-1]:
                print("  <" + str(output_vertices_dict[item.n1]) + "," + str(
                    output_vertices_dict[item.n2]) + ">,")
            print("  <" + str(output_vertices_dict[edges_list[-1].n1]) + "," + str(
                output_vertices_dict[edges_list[-1].n2]) + ">")
        print("}")




from itertools import combinations


def in_embedded_dict(target, dictionary):
    """
    :param target: Node
    :param dictionary: dict - 2 level
    :return: dict
    """
    for sub1_dict in dictionary.values():
        for sub2_dict in sub1_dict.values():
            if target in sub2_dict:
                return sub2_dict[target]
    return None


def gen_graph(street: Street, prev_vertices, count):
    """
    :param street
    :param prev_vertices: dict of previously generated vertices or empty
    :param count: next index of new vertex
    generate graph from scratch, not incrementally
    """
    street_lns = street.to_line()
    graph = Graph()
    vertices = graph.vertices
    edges = graph.edges

    # add vertices
    for pair in combinations(street_lns.items(), 2):
        i = 0
        for seg1 in pair[0][1]:
            i += 1
            j = 0
            for seg2 in pair[1][1]:
                j += 1
                street1 = pair[0][0]
                street2 = pair[1][0]
                street1_points = {seg1.n1, seg1.n2}
                street2_points = {seg2.n1, seg2.n2}
                intersections = {}
                if seg1.lns_on_same_line(seg2):
                    if seg1.same_line_intersects(seg2):
                        intersections = seg1.overlaps(seg2)
                elif seg1.is_intersected(seg2):
                    intersections = {intersect(seg1, seg2)}
                else:
                    continue
                for intersection in intersections:
                    street1_points.add(intersection)
                    street2_points.add(intersection)

                # generate V
                points1 = {(street1, i): street1_points,
                           (street2, j): street2_points}  # val: set()
                for street_points in points1.items():
                    tmp_street = street_points[0][0]
                    tmp_seg = street_points[0][1]
                    tmp_points = street_points[1]
                    for point in tmp_points:
                        # if not in_embedded_dict(point, vertices):
                        if tmp_street not in vertices:
                            vertices[tmp_street] = dict()
                        if tmp_seg not in vertices[tmp_street]:
                            vertices[tmp_street][tmp_seg] = dict()
                        point_ref = in_embedded_dict(point, vertices)
                        if point_ref is None:
                            if point in prev_vertices:
                                point_ref = prev_vertices[point]
                                vertices[tmp_street][tmp_seg][point] = point_ref
                            else:
                                vertices[tmp_street][tmp_seg][point] = count
                                count += 1
                        else:
                            vertices[tmp_street][tmp_seg][point] = point_ref

    # generate E
    for sub1_dict in vertices.values():
        for sub2_dict in sub1_dict.values():
            same_seg_points = sorted(list(sub2_dict.keys()))
            for idx, point in enumerate(same_seg_points[:-1]):
                edges.add(Line(point, same_seg_points[idx + 1]))

    return graph, count


def main():
    streets = Street()
    graph = Graph()
    count = 1

    line = 'a'
    while True:
        try:
            line = sys.stdin.readline().strip()
            if line == '':
                # sys.stderr.write('Program exiting on empty string')
                break

            # process the input and perform logic
            in_word: InputContent = process_input(line)
            # INPUT DEBUG
            # print(in_word.__dict__)  # debug input

            if not in_word.status:
                continue

            if in_word.cmd == 'gg':
                prev_vert = graph.gen_output_vertices_dict()
                graph, count = gen_graph(streets, prev_vert, count)
                graph.output()
            elif in_word.cmd == 'add':
                streets.add(in_word.street_name, in_word.coordinates)
            elif in_word.cmd == 'mod':
                streets.modify(in_word.street_name, in_word.coordinates)
            elif in_word.cmd == 'rm':
                streets.remove(in_word.street_name)
            else:
                print(f'Error: your command "{line}" was not understood', file=sys.stderr)

        except Exception as e:
            print(f'Error: received unhandled exception, continue operation {e}', file=sys.stderr)


if __name__ == "__main__":
    main()
