import heapq
from itertools import count

from tiratiivistys.classes import Node, Weight


class NodeQueue:
    def __init__(self, weights: list[Weight], Node: Node) -> None:
        self.__Node = Node
        self.__counter = count()
        self.__pq = [(weight, self.__tiebreaker, self.__Node(byte))
                     for (byte, weight)
                     in weights]
        self.__leaf_nodes = [node for _, _, node in self.__pq]

        self.__push = lambda item: heapq.heappush(self.__pq, item)
        self.__pop = lambda: heapq.heappop(self.__pq)

        self.__parse = lambda item: {"weight": item[0], "node": item[-1]}
        self.__get = lambda items, key: tuple((self.__parse(item)[key]
                                               for item
                                               in items))
        self.__nodes = lambda items: self.__get(items, "node")
        self.__combined_weight = lambda items: sum(self.__get(items, "weight"))

        heapq.heapify(self.__pq)
        while self.__length > 1:
            self.__push_combined(*self.__pop_two())

    @property
    def __length(self) -> int:
        return len(self.__pq)

    @property
    def __tiebreaker(self) -> int:
        return next(self.__counter)

    def __push_combined(self, *two_smallest: tuple[tuple]) -> None:
        left, right = self.__nodes(two_smallest)
        node = self.__Node()
        node.adopt(left, right)
        self.__push((self.__combined_weight(two_smallest),
                     self.__tiebreaker,
                     node))

    def __pop_two(self) -> tuple[tuple]:
        return self.__pop(), self.__pop()

    @property
    def root(self) -> Node:
        return self.__parse(self.__pop())["node"]

    @property
    def leaves(self) -> Node:
        return {getattr(node, "value"): node
                for node
                in self.__leaf_nodes}
