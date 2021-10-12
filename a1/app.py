#!/usr/bin/env python3
import sys
from input import process_input, InputContent
from graph import Graph
from graph_gen import gen_graph
from street import Street


# YOUR CODE GOES HERE


def main():
    streets = Street()
    graph = Graph()
    count = 1

    line = 'a'
    while True:
        try:
            line = sys.stdin.readline().strip()
            if line == '':
                sys.stderr.write('Program exiting on empty string')
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
                print(f'Error: your command "{line}" was not understood')

        except Exception as e:
            print(f'Error: received unhandled exception, continue operation {e}')


# if __name__ == "__main__":
#     # given test:
#     streets = Street()
#     graph = Graph()
#     count = 1
#
#     # Given sample test
#     streets.add('Weber Street', [Node(2, -1), Node(2, 2), Node(5, 5), Node(5, 6), Node(3, 8)])
#     streets.add('King Street', [Node(4, 2), Node(4, 8)])
#     streets.add('Davenport Road', [Node(1, 4), Node(5, 8)])
#
#     prev_vert = graph.gen_output_vertices_dict()
#     graph, count = gen_graph(streets, prev_vert, count)
#     graph.output()
