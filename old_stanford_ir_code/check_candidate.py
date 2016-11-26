import sys 

fn1, fn2, w1, w2 = sys.argv[1].split(",")

c1s = []
c2s = []

with open("shingles.congress.sorted", "r") as inf:
    for rw in inf:
        fn, digit, window, window_size, iter_ = rw.replace("\n", "").split(",")
        if (fn == fn1 and window == w1):
            c1s.append(digit)
        if (fn == fn2 and window == w2):
            c2s.append(digit)


overlap = len(set(c1s).intersection(set(c2s)))

with open("shingles.congress.candidates.jacs", "a") as outf:
    outf.write(sys.argv[1] + "," + str(overlap) + "\n")