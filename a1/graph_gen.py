from street import Street
from graph import Graph
from line import Line, intersect
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
