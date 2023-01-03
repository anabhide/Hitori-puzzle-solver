from hitori_grid import HitoriGrid
import random

def select_variable(grid):

    for i in (range(grid.get_width())):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) > 1:
                return i, j

    return None


def search(hgrid, var_selector):

    if hgrid.single_variable():
        # use middle cell to start BFS
        mid = hgrid.get_width() // 2 
        parx = mid
        pary = mid
        if hgrid.get_cells()[mid][mid] == 'X':
            neighbors = hgrid.available_moves(mid, mid)
            parx = neighbors[0][0]
            pary = neighbors[0][1]
        if hgrid.partition(parx, pary):
            return hgrid, False
        else:
            return hgrid, True # return solution if no partition present

    var_i, var_j = var_selector(hgrid)

    for d in hgrid.get_cells()[var_i][var_j]:

        if hgrid.is_value_consistent(d, var_i, var_j):
            copy_hgrid = hgrid.copy()
            copy_hgrid.get_cells()[var_i][var_j] = d
            rb, boolean = search(copy_hgrid, var_selector)   
            if boolean:
                return rb, True

    return hgrid, False


file = open('h8.txt', 'r')
problems = file.readlines()
for p in problems:
    g = HitoriGrid()
    g.read_file(p)

    a, b = search(g, select_variable)
    a.print()
    print('\n')
