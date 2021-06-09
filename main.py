import json
import copy
import numpy as np
import math


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

    # grid = (x2 - x1) / SIZE
    # nx = SIZE + 1
    #
    # DEBUG using fixed grid
    grid = 0.5
    nx = int(round((x2 - x1) / grid)) + 1
    ny = int(round((y2 - y1) / grid)) + 1
    # print("area", x1, y1, x2, y2)
    # print("nx, ny:", nx, ny)
    mat = [[0 for i in range(ny)] for i in range(nx)]
    shift = make_shift(x1, y1, grid)
    for module in jobj["modules"]:
        add_to_matrix(mat, module, layer, shift)
    return mat


def scale(mat, nx_target):
    # scale mat
    nx = len(mat)
    ny = len(mat[0])
    # factor
    factor = nx / (nx_target - 1)
    ny_target = int(round(ny / factor)) + 1
    # print("scaling to ", nx_target, ny_target)
    # new mat
    res = [[set() for _ in range(ny_target)] for _ in range(nx_target)]
    res1 = [[0 for _ in range(ny_target)] for _ in range(nx_target)]

    for i in range(nx):
        for j in range(ny):
            ii = int(round(i / factor))
            jj = int(round(j / factor))
            # print("ii,jj", ii, jj)
            # TODO merge? if two points collapse into 1 index, merge it.
            # e.g. net 5, 8 will merge into '{5,8}'
            #
            # But I'll need to connect the pads, e..g {2,4} should be connected
            # to {2,8} to {8,9}
            #
            # res[ii][jj] += "-" + str(mat[i][j])
            #
            # For now, I'm just replacing it for simplicity. This might create
            # many dangling single nodes
            if mat[i][j] == 1:
                res1[ii][jj] = 1
            elif mat[i][j] == 0:
                pass
            else:
                res[ii][jj].add(mat[i][j])
    # merge
    h = {}

    def find(x):
        if x in h:
            return find(h[x])
        else:
            return x

    def union(x, y):
        x = find(x)
        y = find(y)
        if x != y:
            h[x] = y

    # construct disjoint set
    for row in res:
        for s in row:
            if s:
                x = s.pop()
                for y in s:
                    union(x, y)
                # Add it back, this is ugly
                s.add(x)
    # convert the matrix
    for i in range(len(res)):
        for j in range(len(res[i])):
            if not res[i][j]:
                # 0 or 1
                res[i][j] = res1[i][j]
            else:
                res[i][j] = find(res[i][j].pop())
    return res


def file2mat(fname):
    with open(fname) as fp:
        jobj = json.load(fp)
        for layer in ["F", "B"]:
            mat = board2mat(jobj, 30, layer)
            if mat:
                # mat = twoify(mat)
                # use numpy to save csv
                np.savetxt(
                    fname + "-" + layer + ".csv", np.array(mat), delimiter=",", fmt="%d"
                )
                # twoify:
                np.savetxt(
                    fname + "-" + layer + "-twoify.csv",
                    np.array(twoify(mat)),
                    delimiter=",",
                    fmt="%d",
                )
                # scale to 30 and twoify
                np.savetxt(
                    fname + "-" + layer + "-scaled.csv",
                    np.array(twoify(scale(mat, 30))),
                    delimiter=",",
                    fmt="%d",
                )
                # sampled by index
                # get center
                x, y = np.array(mat).shape
                x = max(int(round(x / 2)) - 15, 0)
                y = max(int(round(y / 2)) - 15, 0)
                sample = np.array(mat)[x : x + 30, y : y + 30].tolist()
                np.savetxt(
                    fname + "-" + layer + "-sampled.csv",
                    np.array(twoify(sample)),
                    delimiter=",",
                    fmt="%d",
                )


if __name__ == "__main__":
    #     file2mat("out.json")
    import argparse

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("jsonfile", metavar="j", type=str, help="json file")

    args = parser.parse_args()
    print("processing ", args.jsonfile, " ..")
    file2mat(args.jsonfile)
