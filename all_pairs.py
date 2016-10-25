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
    for pair in itertools.product(current_list, current_list):
        a, b = pair
        with open("shingles.congress.candidates", "a") as outf:
            outf.write("{},{}\n".format(a, b))

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