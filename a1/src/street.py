from graph import Graph
from node import Node
from line import Line


class Street:
    '''Street class keep track of all entered streets'''

    def __init__(self) -> None:
        self.street_db: dict = dict()

    def add(self, street_name: str, coordinates: list) -> None:
        if street_name not in self.street_db:
            self.street_db[street_name] = coordinates
        else:
            print('ERRROR Street.add(): {street_name} already exists')

    def modify(self, street_name: str, coordinates: list):
        if street_name in self.street_db:
            self.street_db[street_name] = coordinates
        else:
            print('ERRROR Street.modify(): {street_name} does not exists')

    def remove(self, street_name):
        if street_name in self.street_db:
            del self.street_db[street_name]
        else:
            print('ERRROR Street.remove(): {street_name} does not exists')

    def to_line(self):
        street_segs = {}
        for street, coordinates in self.street_db.items():
            print(street, coordinates)
            # segs = []
            segs = set()
            for a, b in zip(coordinates[:-1], coordinates[1:]):
                segs.add(Line(a, b))

            street_segs[street] = segs
        return street_segs

    def generate_graph(self):
        graph = Graph(self.street_db)
        graph.generate_graph()


if __name__ == '__main__':
    st = Street()
    st.add('Cool weeber Street', [Node(1, 2), Node(3, 4), Node(5, 6)])
    print(st.to_line())
