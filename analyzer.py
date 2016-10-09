'''
many docs have lots of passages w/ high jac similarity.
this makes a pass over the file and finds all digits that
overlap across at least 1 file
'''
from __future__ import division
from collections import defaultdict
import os
import itertools
import collections
import ipdb

ITERS = 0

# ye olde logical document
D_i = collections.namedtuple('D_i', 'fn windowno')


def delete_old_stuff():
    '''delete old files'''
    def delete(d):
        try:
            os.remove(d)
        except OSError:
            pass

    to_delete = ["shingles.congress.filtered",
                "congress.control_c.candidates",
                "shingles.congress.filtered_twice"]

    for item in to_delete:
        delete(item)


def make_interesting_digits():
    '''make a list of digits to investigate further'''
    interesting_digits = defaultdict(set)

    with open("shingles.congress", "r") as inf:
        for rw in inf:
            biys = rw.replace("\n", "").split(",")
            fn, digit, window, window_size, iter_ = biys
            interesting_digits[digit].add(fn)
    return interesting_digits


def make_investigate_more_list():
    '''make a list of digits that are even worth looking at'''
    investigate_more = []
    interesting_digits = make_interesting_digits()
    for k in interesting_digits:
        if len(interesting_digits[k]) > 1:
            investigate_more.append(k)
    return set(investigate_more)


def make_filtered_file(interesting_digits):
    '''make a filtered file'''
    global ITERS

    with open("shingles.congress", "r") as inf:
        for rw in inf:
            biys = rw.replace("\n", "").split(",")
            fn, digit, window, window_size, iter_ = biys
            if iter_ > ITERS:
                try:
                    ITERS = int(iter_) # there is a header that is not int
                except ValueError:
                    pass
            if digit in interesting_digits:
                with open("shingles.congress.filtered", "a") as outf:
                    outf.write(rw)


def record_pairs(candidates):
    '''
    record all pairs
    '''
    counts = defaultdict(int)
    for combo in itertools.combinations(candidates, 2):
        one, two = combo
        if one.fn != two.fn:
            with open("congress.control_c.candidates", "a") as outf:
                outf.write("{}-{},{}-{}\n".format(one.fn,
                                                one.windowno,
                                                two.fn,
                                                two.windowno))

def filter_again():
    candidates = [c.replace("\n", "") for c in
                 open("congress.control_c.candidates", "r")]

    def include(fn_, window_):
        for c in candidates:
            if fn_ in c and window_ in c:
                return True
        return False

    with open("shingles.congress.filtered", "r") as inf:
        for rw in inf:
            biys = rw.replace("\n", "").split(",")
            fn, digit, window, window_size, iter_ = biys
            if include(fn, window):
                with open("shingles.congress.filtered_twice", "a") as outf:
                    outf.write(rw)

def find_non_trivial_jac_overlap():
    '''loop over a file. ASSUME filtered by digit, aka x^pi_i'''
    x_i_pi = None  # digit in question
    candidate_pairs = []
    with open("shingles.congress.filtered", "r") as inf:
        for rw in inf:
            biys = rw.replace("\n", "").split(",")
            fn, digit, window, window_size, iter_ = biys
            if digit != x_i_pi:
                if x_i_pi is not None:
                    record_pairs(candidate_pairs)
                x_i_pi = digit
                candidate_pairs = []
            d_i = D_i(fn=fn, windowno=window)
            candidate_pairs.append(d_i)


def main():
    '''just main method'''
    print "[*]delete old stuff"
    delete_old_stuff()
    print "[*]find interesting digits"
    digits = make_investigate_more_list()
    print "[*]filter out uninteresting digits"
    make_filtered_file(digits)
    print "[*]find non trivial jac overlaps"
    find_non_trivial_jac_overlap()
    print "[*]filter out anything that is not a candidate"
    filter_again()

main()
