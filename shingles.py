'''support code for shingling'''

import cPickle as pickle
import hashlib
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='')
parser.add_argument('-filename', action="store", dest="filename")
parser.add_argument('-ngram_size', action="store", dest="ngram_size", type=int)
args = parser.parse_args()

HASHLEN = 32

def permute(hashed, pi_):
    '''permute hashed and return a hex string'''
    assert len(hashed) == len(pi_)
    out = ""
    for c_ in range(HASHLEN):
        out += hashed[np.where(pi_ == c_)[0][0]]
    return "0x" + out


def shingle(doc, size):
    '''
    make shingles

    doc is a list of unigrams, ["the", "cat", "sat"]
    '''
    shingles = zip(*[doc[i:] for i in range(size)])
    #import ipdb
    #ipdb.set_trace()
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
    import ipdb
    ipdb.set_trace()
    hdj = [hashlib.md5(s).hexdigest() for s in shingles] # hash
    pi_d_j = [permute(h_, pi) for h_ in hdj]
    return int(min(pi_d_j), 16)

if __name__ == '__main__':
    print shingle_hash_permute_min(["a", "b", "c"], args.ngram_size)