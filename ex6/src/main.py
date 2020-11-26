from typing import List
import numpy as np
from Agent import Agent

"""
    >>> agents_lst = []
    >>> agents_lst.append(Agent([8, 4, 3]))
    >>> agents_lst.append(Agent([5, 8, 3]))
    >>> agents_lst.append(Agent([3, 5, 1]))
    >>> vcg(agents_lst, 3)
"""


def printOutcome(chosen_opt: int, agents_pay: List[Agent]):
    print("The chosen option is {:d}.".format(chosen_opt))
    pay_sum = 0
    for ag_idx, ag in enumerate(agents_pay):
        print("Agent #{:d} pays {:.3f}.".format(ag_idx, ag.pay))
        pay_sum += ag.pay


def vcg(agents: List[Agent], num_options: int):
    """

    :param agents:
    :param num_options:
    :return:

    >>> agents_lst = []; agents_lst.append(Agent([8, 4, 3])); agents_lst.append(Agent([5, 8, 3])); agents_lst.append(Agent([3, 5, 1])); vcg(agents_lst, 3)
    The chosen option is 1.
    Agent #0 pays 4.000.
    Agent #1 pays 6.000.
    Agent #2 pays 4.000.
    """
    opt_mat = np.array([x.values for x in agents])
    chosen_opt = np.argmax(opt_mat.sum(0))

    for idx, agent in enumerate(agents):
        agent.org_pay = agent.value(chosen_opt)

    for idx, agent in enumerate(agents):
        tmp_opt_mat = np.array([x.values for i, x in enumerate(agents) if not i is idx])
        best_op = np.argmax(tmp_opt_mat.sum(0))
        agent.pay = agent.org_pay + tmp_opt_mat.sum(0)[chosen_opt] - tmp_opt_mat.sum(0)[best_op]

    printOutcome(chosen_opt, agents)


def main():
    # Envy Triangle
    agents_lst = []
    agents_lst.append(Agent([8, 4, 3]))
    agents_lst.append(Agent([5, 8, 3]))
    agents_lst.append(Agent([3, 5, 1]))

    vcg(agents_lst, 3)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)