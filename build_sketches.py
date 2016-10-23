# easy to parallelize
import sys
counter = 0
with open(sys.argv[1], "r") as inf:
    for ln in inf:
        counter += 1
        ln = ln.replace("\n", "")
        fn, min_digit, window_no, window_size, iter_no = ln.split(",")
        doc = fn.replace("/", "#") + "_" + window_no
        with open("sketches/" + doc, "a") as outf:
            outf.write(ln + "\n")
        if counter % 1000 == 0:
            print counter
