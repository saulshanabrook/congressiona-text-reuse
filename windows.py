'''take a file and make some windows'''

import argparse
import json
import datetime
import hashlib
import numpy as np
import profile

import cPickle as pickle

import logging
logging.basicConfig(filename='windows.log', level=logging.DEBUG)

def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-size', action="store", dest="size", type=int)
    parser.add_argument('-fn', action="store", dest="fn")
    parser.add_argument('-iter', action="store", dest="iter")
    return parser.parse_args()

args = get_args()

HASHLEN = 32
SHINGLESIZE = 2 # size of shingle, not window!


def find_windows(input_list, n):
    '''find all ngrams'''
    return zip(*[input_list[i:] for i in range(n)])


def get_tokens(fn):
    '''get tokens in file'''
    all_tokens = []
    with open(fn, "r") as inf:
        js = json.load(inf)
        for sentence in js["sentences"]:
            for token in sentence["tokens"]:
                all_tokens.append(token)
    return all_tokens


def permute(hashed, pi_):
    '''permute hashed and return a hex string'''
    assert len(hashed) == len(pi_)
    out2 = [None] * HASHLEN # this could be a global var that keeps getting refilled
    
    for pno, p in enumerate(pi_):
        out2[p] = hashed[pno]
    
    out2 = "".join(out2)
    
    # Old, slower method permute method that I know works below
    #out = ""
    #for c_ in range(HASHLEN):
    #    out += hashed[np.where(pi_ == c_)[0][0]]    
    # assert out == out2

    return "0x" + out2


def shingle(doc, size):
    '''
    make shingles

    doc is a list of unigrams, ["the", "cat", "sat"]
    '''
    shingles = zip(*[doc[i:] for i in range(size)])
    return [" ".join(a) for a in shingles]


def get_pi():
    '''load a permutation from disk'''
    with open("pi.p", "r") as outf:
        return pickle.load(outf)


def shingle_hash_permute_min(doc, ngram_size):
    '''
    - shingle doc, hash shingles, permute the hashes
    - doc is a list of unigrams, ["the", "cat", "sat"]
    - ngram_size = size of ngram
    '''
    pi = get_pi()
    shingles = [" ".join(a) for a in zip(*[doc[i:] for i in range(ngram_size)])]
    hdj = [hashlib.md5(s.encode("ascii", "ignore")).hexdigest() for s in shingles] # hash
    pi_d_j = [permute(h_, pi) for h_ in hdj]
    return int(min(pi_d_j), 16)


# NO WINDOWS
def do_doc_simpler():
    '''
    Bunch o stuff
       - make windows
       - shingle_hash_permute_min them
       - report results to file
    '''
    doc = get_tokens(args.fn)
    min_digit = shingle_hash_permute_min(doc, SHINGLESIZE)
    with open(args.fn.split("/").pop() + ".debug", "a") as outf:
        outf.write(str(min_digit) + "\n")
    logging.debug("{}\t{}\tran permute".format(datetime.datetime.utcnow(), args.fn))


def do_doc():
    '''
    Bunch o stuff
       - make windows
       - shingle_hash_permute_min them
       - report results to file
    '''
    ngrams = find_windows(get_tokens(args.fn), args.size)
    for window_no, window in enumerate(ngrams):
        min_digit = shingle_hash_permute_min(window, SHINGLESIZE)
        with open("shingles.congress", "a") as outf:
            out_str = ",".join([args.fn, str(min_digit), str(window_no), str(args.size), str(args.iter)])
            outf.write(out_str + "\n")
    logging.debug("{}\t{}\tran permute".format(datetime.datetime.utcnow(), args.fn))

def get_window(fn, size, window_no):
    ngrams = find_windows(get_tokens(fn), size)
    return ngrams[window_no]

do_doc_simpler()
# profile.run('do_doc()')

