# Download github repos

Run the following query to GitHub APIs to get a list of repos:

```
curl   -H "Accept: application/vnd.github.v3+json" https://api.github.com/search/repositories?q=stars%3A%3E0+language%3A%22KiCad+Layout%22 > github.json
```

Convert this into github.txt (by some code in `py.ipynb`). Then, run `run.sh` to download into `benchmarks/` folder. The `run.sh` will also invoke `main.rkt` and `main.py` to parse the `kicad_pcb` files in the `benchmarks` folder. The output (csv files) will be put in `output` folder.


