from graph import Graph
from node import Node
from line import Line
from sys import stderr


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


# if __name__ == '__main__':
    # st = Street()
    # st.add('Cool weeber Street', [Node(1, 2), Node(3, 4), Node(5, 6)])
    # print(st.to_line())
