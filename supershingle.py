import sys

def shingle(doc, n):
    shingles = zip(*[doc[i:] for i in range(n)])
    return ["".join(a) for a in shingles]

fn = sys.argv[1]

with open(fn, "r") as inf:
    sketch = []
    for ln in inf:
        ln = ln.replace("\n", "")
        # fn, min_digit, window_no, window_size, iter_no
        tup = tuple(ln.split(","))
        sketch.append(tup)

    sketch.sort(key=lambda x:int(x[1]))

    lowest = shingle([i[1] for i in sketch], 2)
    
    for l in lowest:
        with open("supershingles.txt", "a") as outf:
            outf.write(fn + "," + l + "\n")
