from dataclasses import dataclass
from typing import List

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

np.random.seed(42)
random.seed(42)


class person:
    def __init__(self, p_id, rel):
        self.p_id = p_id
        self.rel = max(rel, 1)


def case1():
    ppl = {
        'a': person('a', 1),
        'b': person('b', 1),
        'c': person('c', 1),
        'd': person('d', 5),
        'e': person('e', 10)
    }

    edges = [
        [ppl['a'], ppl['b']],
        [ppl['c'], ppl['b']],
        [ppl['c'], ppl['d']],
        [ppl['a'], ppl['d']],
        [ppl['a'], ppl['c']],
        [ppl['e'], ppl['b']],
        [ppl['e'], ppl['d']],
        [ppl['e'], ppl['a']],
        [ppl['e'], ppl['c']],

    ]
    return ppl, edges


def case2():
    ABC = 'abcdefghijklmnopqrstuvwxyz'
    np.random.seed(42)
    ppl = {ABC[i]: person(ABC[i], np.random.randint(0, 25)) for i in range(10)}

    edges = [
        [ppl[ABC[np.random.randint(0, len(ppl))]],
         ppl[ABC[np.random.randint(0, len(ppl))]]] for _ in range(10)

    ]
    ppl.pop('g')
    return ppl, edges


def case3():
    ppl = {
        'a': person('a', 11),
        'b': person('b', 1),
        'c': person('c', 1),
        'd': person('d', 1),
        'a1': person('a1', 12),
        'b1': person('b1', 2),
        'c1': person('c1', 1),
        'd1': person('d1', 1),
        'e1': person('e1', 10),
    }

    edges = [
        [ppl['a'], ppl['a1']],
        [ppl['a'], ppl['b1']],
        [ppl['b'], ppl['a1']],
        [ppl['b'], ppl['b1']],
        [ppl['c'], ppl['b1']],
        [ppl['c'], ppl['c1']],
        [ppl['c'], ppl['d1']],
        [ppl['d'], ppl['c1']],
        [ppl['d'], ppl['d1']],
        [ppl['e1'], ppl['d1']],
    ]
    return ppl, edges


def displayMatching(people: dict, edges: List[list]):
    graph = nx.Graph()
    for p in people.values():
        graph.add_node(p.p_id)

    for edge in edges:
        w = edge[0].rel + edge[1].rel
        graph.add_edge(edge[0].p_id, edge[1].p_id, weight=w)

    max_match = nx.maximal_matching(graph)
    max_match_w = nx.max_weight_matching(graph)

    labels = nx.get_edge_attributes(graph, 'weight')
    plt.ion()
    plt.figure()
    plt.title("Max Matching Graph")
    pos = nx.spring_layout(graph, seed=42)
    pos2 = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos=pos, with_labels=True, font_color='w')
    nx.draw_networkx_edges(graph, pos=pos, edgelist=max_match, edge_color='r', width=4)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.figure()
    plt.title("Relative Graph")
    nx.draw(graph, pos=pos2, with_labels=True, font_color='w')
    nx.draw_networkx_edges(graph, pos=pos2, edgelist=max_match_w, edge_color='g', width=4, )
    nx.draw_networkx_edge_labels(graph, pos2, edge_labels=labels)
    plt.ioff()
    plt.show()


def main():
    for ppl, edges in [case1(), case2(), case3()]:
        displayMatching(ppl, edges)


if __name__ == '__main__':
    main()
