def visualize(e, full=False):
    """visualize traffic"""
    occ = e.state.render_occupancy(full=False)
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