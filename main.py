
import json
import copy
import numpy as np

def vis(mat):
    for row in mat:
        for v in row:
            print('{:>2}'.format(v), end=' ')
        print('')

def make_shift(x1, y1, grid):
    def shift(x, y):
        x = round((x - x1) / grid)
        y = round((y - y1) / grid)
        return x, y
    return shift

def add_to_matrix(mat, module, layer, shift):
    for pad in module['pads']:
        if pad['net'] and layer in pad['layers']:
            x = pad['x'] + module['x']
            y = pad['y'] + module['y']
            x, y = shift(x, y)
#             print(x,y)
            mat[x][y] = pad['net']

def twoify(mat):
    # step 1: separate into 2-pairs with string name
    mat = copy.deepcopy(mat)
    h = {}
    recorded = set()
    for row in mat:
        for i in range(len(row)):
            v = row[i]
            if v != 0:
                if v in h:
                    if v in recorded:
                        recorded.remove(row[i])
                    else:
                        h[row[i]] += 1
                        recorded.add(row[i])
                else:
                    h[row[i]] = 1
                    recorded.add(row[i])
                row[i] = str(row[i]) + '-' + str(h[row[i]])
    # step 2: map string names to integer
    h = {}
    ct = 2
    # FIXME I might want to randomly get 2-pairs
    for row in mat:
        for i in range(len(row)):
            v = row[i]
            if v != 0:
                # the recorded ones are not paired
                if v in recorded:
                    h[v] = 1
                # assign a larger number
                elif v not in h:
                    h[v] = ct
                    ct += 1
                row[i] = h[v]  
    return mat

def board2mat(jobj, SIZE, layer):
#     SIZE = 30
    x1, y1, x2, y2 = jobj['area']
    grid = (x2 - x1) / SIZE
    nx = SIZE + 1
    ny = int(round((y2 - y1) / grid)) + 1
    mat = [[0 for i in range(ny)] for i in range(nx)]
    shift = make_shift(x1, y1, grid)
    for module in jobj['modules']:
        add_to_matrix(mat, module, layer, shift)
    return mat


def file2mat(fname):
    with open(fname) as fp:
        jobj = json.load(fp)
        for layer in ['F', 'B']:
            mat = twoify(board2mat(jobj, 30, layer))
            # use numpy to save csv
            np.savetxt(fname + "-" + layer + '.csv', np.array(mat), delimiter=',', fmt="%d")



if __name__ == '__main__':
#     file2mat("out.json")
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('jsonfile', metavar='j', type=str,
                        help='json file')

    args = parser.parse_args()
    print('processing ', args.jsonfile, ' ..')
    file2mat(args.jsonfile)