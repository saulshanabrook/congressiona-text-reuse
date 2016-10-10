'''
2nd analyzer. uses filtered file
'''
import collections, ipdb, itertools
from collections import defaultdict

# ye olde logical document
D_i = collections.namedtuple('D_i', 'fn windowno')
Candidate = collections.namedtuple('Candidate', 'fn1 windowno1 fn2 windowno2')


def process_digit(current_list):
    candidates = []

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
        c1 = []
        c2 = []
        for log_item in current_list:
            fn, digit, window, window_size, iter_ = log_item.split(",")
            if fn == candidate.fn1 and window == candidate.windowno1:
                c1.append(digit)
            elif fn == candidate.fn2 and window == candidate.windowno2:
                c2.append(digit)
        if len(set(c1).intersection(set(c2))) > 5:
            print len(set(c1).intersection(set(c2)))



def find_jacs():
    current_digit = None
    current_list = []
    counter = 0
    with open("shingles.congress.sorted", "r") as inf:
        for rw in inf:
            counter += 1
            if counter % 100000 == 0:
                print counter
            biys = rw.replace("\n", "")
            fn, digit, window, window_size, iter_ = biys.split(",")
            if digit != current_digit:
                process_digit(current_list)
                current_list = []
                current_digit = digit
            current_list.append(biys)
    process_digit(current_list)

find_jacs()