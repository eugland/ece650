
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


# # for test only - test graph.output()
# graph = Graph()
# # graph.vertices = {1: (1, 2), 2: (2, 3), 3: (3, 4)}
# # graph.edges = [(1, 3), (2, 3)]
# graph.vertices = {1: [1, 2], 2: [2, 3], 3: [3, 4]}
# graph.edges = [[1, 3], [2, 3]]
# graph.output()
