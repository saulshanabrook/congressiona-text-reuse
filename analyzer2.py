'''
2nd analyzer. uses filtered file
'''
import collections, ipdb, itertools, os, sys
from collections import defaultdict

# ye olde logical document
D_i = collections.namedtuple('D_i', 'fn windowno')
Candidate = collections.namedtuple('Candidate', 'fn1 windowno1 fn2 windowno2')

try:
    os.remove("shingles.congress.candidates")
except OSError:
    print "could not find old candidates file to delete"


def get_jac(fn1, fn2, window1, window2):
    fn1 = fn1.replace("/", "#").replace(".anno", "")
    fn2 = fn2.replace("/", "#").replace(".anno", "")
    s1 = set([l.replace("\n", "").split(",")[1] for l in open("sketches/{}.anno_{}".format(fn1, window1))])
    s2 = set([l.replace("\n", "").split(",")[1] for l in open("sketches/{}.anno_{}".format(fn2, window2))])
    return len(s1.intersection(s2))



def process_digit(current_list):
    '''find reasonable comparisons based on information from this digit'''
    candidates = []

    # all files for just one digit
    assert len(set([a.split(",")[1] for a in current_list])) < 2
    # find resonable candidates
    for log_item in current_list:
        fn, digit, window, window_size, iter_ = log_item.split(",")
        candidates.append(D_i(fn=fn, windowno=window))
    
    reasonable_candidates = []
    for pair in itertools.product(candidates, candidates):
        a, b = pair
        if a.fn != b.fn:
            c = Candidate(fn1=a.fn, fn2=b.fn, windowno1=a.windowno, windowno2=b.windowno)
            reasonable_candidates.append(c)
    for candidate in reasonable_candidates:
        jac = get_jac(candidate.fn1, candidate.fn2,candidate.windowno1,candidate.windowno2)
        with open("shingles.congress.candidates", "a") as outf:
            outf.write("{},{},{},{},{}\n".format(candidate.fn1,
                                              candidate.fn2,
                                              candidate.windowno1,
                                              candidate.windowno2,
                                              jac))


def find_candidates():
    current_digit = None
    current_list = []
    counter = 0
    with open("shingles.congress.sorted", "r") as inf:
        for rw in inf:
            counter += 1
            if counter % 1000 == 0:
                sys.stderr.write("{}\t".format(counter))
            biys = rw.replace("\n", "")
            fn, digit, window, window_size, iter_ = biys.split(",")
            if digit != current_digit:
                process_digit(current_list)
                current_list = []
                current_digit = digit
            current_list.append(biys)
    process_digit(current_list)


if __name__ == '__main__':
    find_candidates()