'''
2nd analyzer. uses filtered file
'''
import collections, itertools, os, sys
from collections import defaultdict

# ye olde logical document
D_i = collections.namedtuple('D_i', 'fn windowno')
Candidate = collections.namedtuple('Candidate', 'fn1 windowno1 fn2 windowno2')


def process_digit(current_list):
    '''find reasonable comparisons based on information from this digit'''
    candidates = []
    if len(current_list) == 1:
        return

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
        with open("shingles.congress.candidates", "a") as outf:
            outf.write("{},{},{},{}\n".format(candidate.fn1,
                                              candidate.fn2,
                                              candidate.windowno1,
                                              candidate.windowno2))

import re
digitgetter = re.compile("(?<=,)[0-9]+")

incomingfn = sys.argv[1]

def find_candidates():
    current_digit = None
    current_list = []
    counter = 0
    with open(incomingfn, "r") as inf:
        for rw in inf:
            counter += 1
            if counter % 1000 == 0:
                with open(incomingfn + ".log", "a") as outf:
                    outf.write(incomingfn + "_" + str(counter) + "\n")
            biys = rw.replace("\n", "")
            digit = digitgetter.search(biys).group(0)
            if digit != current_digit:
                process_digit(current_list)
                current_list[:] = []
                current_digit = digit
            current_list.append(biys)
    process_digit(current_list)


if __name__ == '__main__':
    find_candidates()