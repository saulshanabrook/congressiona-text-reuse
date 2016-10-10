'''
2nd analyzer. uses filtered file
'''
import collections, ipdb, itertools
from collections import defaultdict

# ye olde logical document
D_i = collections.namedtuple('D_i', 'fn windowno')


def process_digit(current_list):
    candidates = []

    for c in current_list:
        fn, digit, window, window_size, iter_ = c.split(",")
        try:
            fn = fn.split(":").pop()
        except:
            pass
        candidates.append(D_i(fn=fn, windowno=window))
    
    for pair in itertools.product(candidates, candidates):
        a, b = pair
        if a.fn != b.fn:
            print a.fn, b.fn


def find_jacs():
    current_digit = None
    current_list = []
    with open("shingles.congress.sorted", "r") as inf:
        for rw in inf:
            biys = rw.replace("\n", "")
            fn, digit, window, window_size, iter_ = biys.split(",")
            if digit != current_digit:
                process_digit(current_list)
                current_list = []
                current_digit = digit
            current_list.append(biys)
    process_digit(current_list)

find_jacs()