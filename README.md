# Intro to the code

The `main.rkt` file takes a `.kicad_pcb` file and outputs a `.json` file
containing all the modules (e.g. resistors, ICs).
The `main.py` file takes the `.json` file and generate input matrix. The
`run.sh` is a script to scan the filesystem for `.kicad_pcb` files and run the
`main.rkt` and `main.py` in batches.

Notable functions in `main.py`:

- `board2mat`: from json object to matrix
- `twoify`: the matrix might contain multiple-pad nets. This break them into
  2-pad nets. E.g. a 7-pad net will be broken into three 2-pad nets, and the
  last pad is discarded.
- `scale`: scale a matrix to desired size. If two pads collapsed into one
  position, the nets are **merged**, by union & find (disjoint set) algorithm.
  Of course, this will produce muti-pad nets, so call `twoify` to break them.

The `file2mat` contains examples of how to generate different variations of the
data. E.g.

```py
# original matrix
mat = board2mat(jobj, 'F')
# twoified matrix
mat1 = twoify(mat)
# scaled and twoified matrix
mat2 = twoify(scale(mat, 30))
# sampled and twoified matrix
sample = np.array(mat)[x : x + 30, y : y + 30]
mat3 = twoify(sample)
```

# Run the code

```sh
racket main.rkt /path/to/xxx.kicad_pcb /path/to/output.json # => generate output.json
python3 main.py /path/to/output.json # => generate csv files in output/ folder
# or use wrapper script
bash run.sh
```

# Download github repos

Run the following query to GitHub APIs to get a list of repos:

```
curl   -H "Accept: application/vnd.github.v3+json" https://api.github.com/search/repositories?q=stars%3A%3E0+language%3A%22KiCad+Layout%22 > github.json
```

Convert this into github.txt (by some code in `py.ipynb`). Then, run `run.sh` to download into `benchmarks/` folder. The `run.sh` will also invoke `main.rkt` and `main.py` to parse the `kicad_pcb` files in the `benchmarks` folder. The output (csv files) will be put in `output` folder.
