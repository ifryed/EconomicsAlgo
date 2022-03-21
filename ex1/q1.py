import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig = None


class Round:
    count = 0

    def __init__(self, h_s, h_e, w_s, w_e, players):
        self.r_count = Round.count
        self.h_s = h_s
        self.h_e = h_e
        self.w_s = w_s
        self.w_e = w_e
        self.players = players
        Round.count += 1


def main():
    global ix, iy, players, h, w, ax
    global coords, winners

    area = 4000
    h = area // np.sqrt(area)  # np.random.randint(1, area / 2)
    w = area / h
    players = ['p_{}'.format(x) for x in range(4)]
    rounds = [Round(0, h, 0, w, players)]
    print(players)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    winners = []
    while rounds:
        tmp_round = rounds.pop(0)
        print("Round:", tmp_round.r_count)
        tmp_players = list(tmp_round.players)

        w_s, w_e = tmp_round.w_s, tmp_round.w_e
        h_s, h_e = tmp_round.h_s, tmp_round.h_e
        coords = []
        while tmp_players:
            cur_player = tmp_players.pop(0)
            print("Player", cur_player)
            plt.xlim(-10, w + 10)
            plt.ylim(-10, h + 10)

            ax.set_title('Player:{} out of {}'.format(cur_player, len(tmp_round.players)))
            ax.add_patch(Rectangle((w_s, h_s),
                                   w_e, h_e,
                                   fc='g',
                                   fill=True,
                                   ec='g',
                                   lw=1))
            print((w_s, h_s), (w_e, h_e))
            plt.pause(0.1)

            def onclick(event):
                global coords
                ix, iy = event.xdata, event.ydata

                if ix < w_s or ix > w_e:
                    return None

                if cur_player in [c[0] for c in coords]:
                    return None
                coords.append((cur_player, (ix, iy)))
                print('x = %d, y = %d' % (
                    ix, iy))

                plt.plot([ix, ix], [0, h], '-')

                plt.pause(0.1)
                if len(tmp_players) == 0:
                    mean = np.array([c[1][0] for c in coords]).mean()
                    p1 = [c[0] for c in coords if c[1][0] <= mean]
                    p2 = [c[0] for c in coords if c[1][0] > mean]

                    for pp in [p1, p2]:
                        if len(pp) == 1:
                            winners.append((pp[0], h_s, h_e, w_s, w_e))
                        else:
                            rounds.append(Round(h_s, h_e, w_s, mean, pp))
                    coords = []
                    plt.cla()

                plt.pause(1)
                return coords

            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            plt.waitforbuttonpress(0)

    print("End")
    print(winners)


if __name__ == '__main__':
    main()
