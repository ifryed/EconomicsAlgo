from typing import List

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from Agent import Agent


def getItemsValue(items: List[int], agent: Agent) -> float:
    tot_val = 0.
    for item in items:
        tot_val += agent.item_value(item)
    return tot_val


def envy_graph(agents: List[Agent], bundle_mat: List[List[int]]) -> nx.Graph:
    en_v_graph = nx.DiGraph()

    # Get each agent's value
    for a_idx, agent in enumerate(agents):
        en_v_graph.add_node(a_idx)
        agent.value = getItemsValue(bundle_mat[a_idx], agent)

    # For each agent, check envy
    for a_idx, agent in enumerate(agents):
        for oa_idx, o_agent in enumerate(agents):
            if a_idx is oa_idx:
                continue
            oa_value = getItemsValue(bundle_mat[oa_idx], agent)
            if oa_value > agent.value:
                en_v_graph.add_weighted_edges_from([(a_idx, oa_idx, oa_value)])

    return en_v_graph


def dispGraph(title, val_mat, bundle_mat):
    n_players, n_items = val_mat.shape
    agents = []
    for i in range(n_players):
        agents.append(Agent(val_mat[i, :]))

    e_graph = envy_graph(agents, bundle_mat)

    # Display Graph
    plt.title(title)
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in e_graph.edges(data=True)])
    node_labels = {i: ("Agent:{:d},V({:})".format(i, x.value)) for i, x in enumerate(agents)}
    pos = nx.nx.spring_layout(e_graph)
    nx.draw_networkx_edge_labels(e_graph, pos, edge_labels=edge_labels)
    nx.draw_networkx(e_graph, pos=pos, with_labels=True,
                     labels=node_labels,
                     font_color='black',
                     font_weight='bold', arrows=True, arrowsize=20, edge_color='red', node_color='yellow')

    plt.show()


def main():
    # Envy Triangle
    val_mat = np.array([
        [1, 1, 1, 2, 1, 0],
        [1, 1, 1, 2, 1, 3],
        [10, 1, 1, 2, 1, 3],
    ])

    bundle_mat = [
        [0, 1],
        [2, 3],
        [4, 5]
    ]
    dispGraph("Triangle", val_mat, bundle_mat)

    # Mexican Standoff
    val_mat = np.array([
        [1, 1, 10, 10, 10, 10],
        [10, 10, 1, 1, 10, 10],
        [10, 10, 10, 10, 1, 1],
    ])

    bundle_mat = [
        [0, 1],
        [2, 3],
        [4, 5]
    ]
    dispGraph("Mexican Standoff", val_mat, bundle_mat)

    # Richi-Rich
    val_mat = np.array([
        [1, 1, 1, 1, 10, 10],
        [1, 1, 1, 1, 10, 10],
        [1, 1, 1, 1, 10, 10],
    ])

    bundle_mat = [
        [0, 1],
        [2, 3],
        [4, 5]
    ]
    dispGraph("Richi-Rich", val_mat, bundle_mat)


if __name__ == '__main__':
    main()
