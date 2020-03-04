import numpy as np

from config import *


def visualize(e, full=False):
    """visualize traffic in ascii mode (terminal output)"""
    occ = e.state.render_occupancy(full=full)
    occ = list(occ)

    # replace character
    replace_chr = {
        0: '_',
        1: 'X',
        2: 'O',
    }
    occ = [[replace_chr[occ[i][j]] for j in range(len(occ[i]))] for i in range(len(occ))]

    # display
    for occ_y in occ[::-1]:
        for occ_x in occ_y:
            print(occ_x, end=' ')
        print('\n')

    return


def render_image(e, full=False):
    occ = e.state.render_occupancy(full=full).T
    img = np.zeros((occ.shape[0] * HEIGHT_SCALE, occ.shape[1] * WIDTH_SCALE))

    for r, row in enumerate(occ):
        for l, lane in enumerate(row):
            img[r * HEIGHT_SCALE: (r + 1) * HEIGHT_SCALE, l * WIDTH_SCALE: (l + 1) * WIDTH_SCALE] = occ[r, l]

    return img
