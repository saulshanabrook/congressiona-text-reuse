'''
THIS IS DEAD CODE DELETE DELETE 10.9
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
                "shingles.congress.filtered_twice",
                "jaccards",
                "shingles.congress.filtered.sorted"]

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
    with open("shingles.congress", "r") as inf:
        for rw in inf:
            biys = rw.replace("\n", "").split(",")
            fn, digit, window, window_size, iter_ = biys
            if digit in interesting_digits:
                with open("shingles.congress.filtered", "a") as outf:
                    outf.write(rw)


def main():
    '''just main method'''
    print "[*]delete old stuff"
    delete_old_stuff()
    print "[*]find interesting digits"
    digits = make_investigate_more_list()
    print "[*]filter out uninteresting digits"
    make_filtered_file(digits)

main()
