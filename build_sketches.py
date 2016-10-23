# easy to parallelize
import sys
with open(sys.argv[1], "r") as inf:
    for ln in inf:
        ln = ln.replace("\n", "")
        fn, min_digit, window_no, window_size, iter_no = ln.split(",")
        doc = fn.replace("/", "#") + "_" + window_no
        with open("sketches/" + doc, "a") as outf:
            outf.write(ln + "\n")
