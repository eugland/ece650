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
