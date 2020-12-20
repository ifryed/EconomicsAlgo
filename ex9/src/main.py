from typing import Set, List

from networkx import DiGraph
import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np

random.seed(42)
np.random.seed(42)

from itertools import chain, combinations


def powerset(iterable):
    """
    Generates the all the sub-groups of a givan list
    Taken from pythons' itertools
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    :param iterable the list
    """

    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def optimal_order(road_graph: DiGraph, source: str, targets: Set[str], verbos=False) -> (List[str], float):
    """
    Returns the optimal order to travel throughout the nodes

    :param road_graph: A directed-graph (Networkx)
    :param source: First and last node
    :param targets: A set of all the nodes that the path must past through
    :param verbos: If True, will plot the dynamic matrix
    :return: The optimal path and total weight
    """
    if len(targets) < 1:
        return [], 0
    targets = list(targets)
    ext_targets = [source] + targets
    dyn_mat = np.ones((len(ext_targets), len(ext_targets))) * float('inf')

    # All Nods to all Nods
    cross_path_mat = np.ones((len(ext_targets), len(ext_targets))) * float('inf')
    cross_fullpath_mat = np.ndarray((len(ext_targets), len(ext_targets)), dtype=object)
    for i, v in enumerate(ext_targets):
        for j, jv in enumerate(ext_targets):
            if j == i:
                continue
            if nx.has_path(road_graph, v, jv):
                cross_path_mat[i, j] = nx.dijkstra_path_length(road_graph, v, jv)
                cross_fullpath_mat[i, j] = nx.dijkstra_path(road_graph, v, jv)[1:]

    # Fill in the last line
    dyn_mat[-1, :] = cross_path_mat[:, 0]
    # Fill the rest of the matrix dynamically
    for row in range(len(ext_targets) - 2, -1, -1):
        for col in range(len(ext_targets)):
            dists = cross_path_mat[col, :] + dyn_mat[row + 1, :]
            min_dist = min(dists)
            dyn_mat[row, col] = min_dist

    if verbos:
        plt.imshow(dyn_mat)

    path = [source]
    last_idx = 0
    path_weight = 0
    if len(targets) == 1:
        min_step = np.argmin(dyn_mat[1, :])
        path += cross_fullpath_mat[last_idx, min_step]
        path += cross_fullpath_mat[min_step, last_idx]
        path_weight += cross_path_mat[last_idx, min_step]
        path_weight += cross_path_mat[min_step, last_idx]
        return path, path_weight

    dyn_mat[:, 0] = float('inf')  # Block the algorithm from choosing the source again
    for k in range(len(ext_targets)):
        min_step = np.argmin(dyn_mat[k, :])  # Find the minimum step
        dyn_mat[:, min_step] = float('inf')  # Block the algorithm from choosing the same node again again
        path += cross_fullpath_mat[last_idx, min_step]
        path_weight += cross_path_mat[last_idx, min_step]
        last_idx = min_step
        if verbos:
            plt.plot(min_step, k, '*r')

    if verbos:
        print("Path Wieght: {:.3f}".format(path_weight))
        plt.xlabel(ext_targets)
    return path, path_weight


def optimal_order_two(road_graph: DiGraph, source: str, targets: Set[str]) -> List[tuple]:
    """
    Returns the optimal order to travel throughout the nodes.
     The function checks whether it is faster to
    split the path in to two cabs or stay with one.

    :param road_graph: A directed-graph (Networkx)
    :param source: First and last node
    :param targets: A set of all the nodes that the path must past through
    :return: The optimal path or paths and total weight
    """
    best_score = float('inf')
    best_way = None
    for s in powerset(targets):
        s = set(s)
        not_s = targets - s
        # Checking set A
        path_1, weight1 = optimal_order(road_graph, source, s)

        # Checking set B
        path_2, weight2 = optimal_order(road_graph, source, not_s)
        score = weight1 + weight2

        if best_score >= score:
            best_score = score
            best_way = [(path_1, weight1),
                        (path_2, weight2)]
    if len(best_way[1][0]) is 0:
        return best_way[:1]
    return best_way


def main():
    road_graph = DiGraph(name='Road Graph')
    roads = [
        ('0', 'a', 1),
        ('a', 'c', 1),
        ('c', 'a', 1),
        ('c', '0', 19),
        ('0', 'd', 3),
        ('d', '0', 3),
        ('d', 'b', 7),
        ('b', 'c', 7),
        ('a', '0', 9),
    ]
    road_graph.add_weighted_edges_from(roads)
    src = '0'
    trgs = {'a', 'b', 'c', 'd'}
    # trgs = {'a', 'd', 'c'}
    # path, weights = optimal_order(road_graph, src, trgs)
    # print('->'.join(path))
    # print("Weight:{:.3f}".format(weights))

    best = optimal_order_two(road_graph, src, trgs)
    tot = 0
    for i, path in enumerate(best):
        print('Path {}'.format(i))
        print('\t', end='')
        print('->'.join(path[0]))
        print('\t', end='')
        print("Weight: {:.3f}".format(path[1]))
        tot += path[1]
    print("Total Weight:{:.3f}".format(tot))

    plt.figure()
    nx.draw(road_graph, with_labels=True)

    plt.show()


if __name__ == '__main__':
    main()
