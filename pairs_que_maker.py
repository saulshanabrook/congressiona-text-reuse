'''just take a single file and add it to the pairs queue'''
import sys, itertools

lns = []

def process_digit(current_list):
    '''find reasonable comparisons based on information from this digit'''
    for pair in itertools.product(current_list, current_list):
        a, b = pair
        one = a.split(",")[0].replace("/", "#")
        two = b.split(",")[0].replace("/", "#")
        w1 = a.split(",")[2].replace("/", "#")
        w2 = b.split(",")[2].replace("/", "#")
        with open("shingles.congress.candidates", "a") as outf:
            outf.write("{},{},{}\n".format(sys.argv[1], "sketches/" + one + "_" + w1, "sketches/" + two + "_" + w2))

with open(sys.argv[1], "r") as inf:
    for ln in inf:
        lns.append(ln.replace("\n", ""))
    process_digit(lns)

