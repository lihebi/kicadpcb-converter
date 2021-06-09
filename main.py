import json
import copy
import numpy as np


def vis(mat):
    for row in mat:
        for v in row:
            print("{:>2}".format(v), end=" ")
        print("")


def make_shift(x1, y1, grid):
    def shift(x, y):
        x = round((x - x1) / grid)
        y = round((y - y1) / grid)
        return x, y

    return shift


def add_to_matrix(mat, module, layer, shift):
    for pad in module["pads"]:
        if layer in pad["layers"]:
            x = pad["x"] + module["x"]
            y = pad["y"] + module["y"]
            x, y = shift(x, y)
            if pad["net"]:
                mat[x][y] = pad["net"]
            else:
                # thet net is not connected, set to 1
                mat[x][y] = 1


# twoify(mat[10:40][15:45])


def twoify(mat):
    # step 1: separate into 2-pairs with string name
    mat = copy.deepcopy(mat)
    h = {}
    recorded = set()
    for row in mat:
        for i in range(len(row)):
            v = row[i]
            if v != 0 and v != 1:
                if v in h:
                    if v in recorded:
                        recorded.remove(v)
                    else:
                        h[v] += 1
                        recorded.add(v)
                else:
                    h[v] = 1
                    recorded.add(v)
                row[i] = str(v) + "-" + str(h[v])
    # single ones
    singles = set()
    for v in recorded:
        singles.add(str(v) + "-" + str(h[v]))
    # step 2: map string names to integer
    h = {}
    ct = 2
    # FIXME I might want to randomly get 2-pairs
    for row in mat:
        for i in range(len(row)):
            v = row[i]
            if v != 0 and v != 1:
                # the recorded ones are not paired
                if v in singles:
                    h[v] = 1
                # assign a larger number
                elif v not in h:
                    h[v] = ct
                    ct += 1
                row[i] = h[v]
    return mat


def board2mat(jobj, SIZE, layer):
    #     SIZE = 30
    # FIXME the module center might be outside this area
    # x1, y1, x2, y2 = jobj["area"]
    #
    # I'm going to use just the modules instead. So get the smallest and largest
    # x and y, and inflate by 10% each side.
    xs = []
    ys = []
    for module in jobj["modules"]:
        for pad in module["pads"]:
            xs.append(module["x"] + pad["x"])
            ys.append(module["y"] + pad["y"])
    if not xs or not ys:
        print("Warning: no pads found")
        return None
    x1 = min(xs)
    y1 = min(ys)
    x2 = max(xs)
    y2 = max(ys)
    # inflat by 10%
    dx = x2 - x1
    dy = y2 - y1
    x1 -= dx * 0.1
    x2 += dx * 0.1
    y1 -= dy * 0.1
    y2 += dy * 0.1

    grid = (x2 - x1) / SIZE
    nx = SIZE + 1
    ny = int(round((y2 - y1) / grid)) + 1
    print("area", x1, y1, x2, y2)
    print("nx, ny:", nx, ny)
    mat = [[0 for i in range(ny)] for i in range(nx)]
    shift = make_shift(x1, y1, grid)
    for module in jobj["modules"]:
        add_to_matrix(mat, module, layer, shift)
    return mat


def file2mat(fname):
    with open(fname) as fp:
        jobj = json.load(fp)
        for layer in ["F", "B"]:
            mat = board2mat(jobj, 30, layer)
            if mat:
                mat = twoify(mat)
                # use numpy to save csv
                np.savetxt(
                    fname + "-" + layer + ".csv", np.array(mat), delimiter=",", fmt="%d"
                )


if __name__ == "__main__":
    #     file2mat("out.json")
    import argparse

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("jsonfile", metavar="j", type=str, help="json file")

    args = parser.parse_args()
    print("processing ", args.jsonfile, " ..")
    file2mat(args.jsonfile)
