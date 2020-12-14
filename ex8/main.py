from Uniform import Uniform


def max_revenue_auction(agent1: Uniform, value1: float) -> float:
    """
    Returns the price to pay for a given Agent and a value
    :param agent1: An agent of type Uniform
    :param value1: The value he is willing to pay
    :return: The final price he is to pay

    >>> agent1 = Uniform(10, 30)
    >>> max_revenue_auction(agent1, 15)
    15.0
    >>> max_revenue_auction(agent1, 10)
    0.0
    """

    r_val = agent1.r(value1)
    return 0.0 if r_val < 0 else agent1.r_inv(0)


def max_revenue_auction2(agent1: Uniform, agent2: Uniform,
                         value1: float, value2: float):
    """
    Returns the price to pay for a given Agent and a value
    :param agent1: Agent #1 of type Uniform
    :param agent1: Agent #2 of type Uniform
    :param value1: The value Agent #1 is willing to pay
    :param value2: The value Agent #2 is willing to pay
    :return: The final price he is to pay

    >>> agent1 = Uniform(10, 30)
    >>> agent2 = Uniform(20, 40)
    >>> max_revenue_auction2(agent1, agent2, 23, 27)
    Agent 1 wins and pays 22.0
    >>> max_revenue_auction2(agent1, agent2, 19, 29)
    Agent 2 wins and pays 24.0
    >>> max_revenue_auction2(agent1, agent2, 12, 19)
    No agent wins
    """

    r1_val = agent1.r(value1)
    r2_val = agent2.r(value2)

    if r1_val > r2_val and r1_val > 0:
        print("Agent 1 wins and pays", max(agent1.r_inv(0), agent1.r_inv(r2_val)))
    elif r2_val > r1_val and r2_val > 0:
        print("Agent 2 wins and pays", max(agent2.r_inv(0), agent2.r_inv(r1_val)))
    else:
        print("No agent wins")


def main():
    agent1 = Uniform(10, 30)
    agent2 = Uniform(20, 40)
    # price = max_revenue_auction(agent1, 15)
    # print("Agent 1 Payed: {:.2f}".format(price))

    max_revenue_auction2(agent1, agent2, 12, 19)


if __name__ == '__main__':
    main()

    import doctest

    doctest.testmod(verbose=True)
