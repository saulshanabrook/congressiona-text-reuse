from __future__ import division
import numpy as np
import ujson as json
import hashlib
import ipdb
import cPickle as pickle
import itertools
import glob
import datetime
import pandas as pd
import numpy as np
import os
from pi import make_pi
import logging
logging.basicConfig(filename='windows.log', level=logging.DEBUG)

# http://nlp.stanford.edu/IR-book/html/htmledition/near-duplicates-and-shingling-1.html

HASH_LEN = 32
SHINGLESIZE = 2

def get_stops():
    import string
    from stop_words import get_stop_words
    return set([a for a in string.punctuation] + get_stop_words('en'))
    
STOPS = get_stops()

def make_windows(doc, n):
    '''
    - chunk into n token blocks (at least for now)
    - no rolling windows. too big! something to improve later
    '''
    # https://gist.github.com/moshekaplan/4678925
    for i in xrange(0, len(doc), n):
        yield doc[i:i+n]

def get_window(fn, size, window_no):
    ngrams = make_windows(get_tokens(fn), size)
    return ngrams[window_no]

def shingle(doc, n):
    shingles = zip(*[doc[i:] for i in range(n)])
    return [" ".join(a) for a in shingles]

def get_pi():
    with open("pi.p", "r") as outf:
        return pickle.load(outf)

def permute(hashed, pi_):
    '''permute h and return a hex string'''
    assert len(hashed) == len(pi_)
    out2 = [None] * HASH_LEN # this could be a global var that keeps getting refilled
    
    for pno, p in enumerate(pi_):
        out2[p] = hashed[pno]
    
    return "0x" + "".join(out2)

def shingle_hash_permute_min(tokens):
    '''shingle doc j, hash shingles, permute the hashes'''
    pi = get_pi()
    shingles = shingle(tokens, SHINGLESIZE) # shingle
    hdj = [hashlib.md5(s).hexdigest() for s in shingles] # hash
    pi_d_j = [permute(h, pi) for h in hdj]
    return int(min(pi_d_j), 16)

def sketch_docs():
    '''get N (iters) sketches of docs'''
    out = []
    for i in range(iters):
        out.append([(shingle_hash_permute_min(j), j) for j in range(len(docs))])
    return out

def get_tokens(fn):
    '''get tokens in file'''
    all_tokens = []
    with open(fn, "r") as inf:
        js = json.load(inf)
        for sentence in js["sentences"]:
            for token in sentence["tokens"]:
                if token.lower() not in STOPS:
                    all_tokens.append(token)
    return all_tokens

def do_doc(fn, window_size, iter_no):
    '''
    Bunch o stuff
       - make windows
       - shingle_hash_permute_min them
       - report results to file
    '''
    windows = make_windows(get_tokens(fn), window_size)
    for window_no, window in enumerate(windows):
        min_digit = shingle_hash_permute_min(window)
        with open("shingles.congress", "a") as outf:
            out_str = ",".join([fn, str(min_digit), str(window_no), str(window_size), str(iter_no)])
            outf.write(out_str + "\n")
    logging.debug("{}\t{}\tran permute".format(datetime.datetime.utcnow(), fn))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-iter')
    parser.add_argument('-doc')
    args = parser.parse_args()

    WINDOWSIZE = 50

    do_doc(args.doc, WINDOWSIZE, args.iter)