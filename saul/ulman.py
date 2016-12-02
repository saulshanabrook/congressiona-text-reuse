from __future__ import division
from collections import defaultdict
from stop_words import get_stop_words
import math
import hashlib
import random
import json
import itertools
import cPickle as pickle
import glob
import string
import sys
import numpy as np
import matplotlib.pyplot as plt



# PATHTOBILLS = "test_data/*anno"
PATHTOBILLS = "govtrackdata/*/sections/*anno"
NBILLS = sum(1 for f in glob.glob(PATHTOBILLS))

# implementation of section 3.3 of http://infolab.stanford.edu/~ullman/mmds/ch3.pdf

SEED = 0
generator = random.Random(SEED)

n = 100 # n permutations
bands = 5

'''helper functions'''

def get_stops():
    '''get a set of stop words'''
    return set([a for a in string.punctuation] + get_stop_words('en'))


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


def get_doc(get_this_doc):
    '''get just one document'''
    for fno, f in enumerate(glob.glob(PATHTOBILLS)):
        if get_this_doc == fno:
            return get_tokens(f)
    raise FileNotFoundError('Could not find doc {}'.format(get_this_doc))


def jaccard(d1, d2):
    '''get the actual jaccard between d1 and d2'''
    a = get_doc(d1)
    b = get_doc(d2)
    return len(set(a).intersection(set(b))) / len(set(a).union(set(b)))


STOPS = get_stops()

def get_docs():
    '''get all anno files in PATHTOBILLS'''
    out = []
    V = set()
    for fno, f in enumerate(glob.glob(PATHTOBILLS)):
        toks = get_tokens(f)
        V.update(set(toks))
        out.append(toks)
        if fno % 1000 == 0:
            sys.stderr.write("read {} of {},\t".format(fno, NBILLS))
    return V, out


def estimated_jaccard(d1, d2):
    '''what is the estimated jaccard similarity between d1 and d2?'''

    with open("sig.p", "r") as inf:
        SIG = pickle.load(inf)

    return len(set(SIG[:, d1]).intersection(set(SIG[:, d2]))) / len(set(SIG[:, d1]).union(set(SIG[:, d2])))


def get_pairs():
    '''get all pairs to check'''
    with open("buckets.p", "r") as inf:
        buckets = pickle.load(inf)

    out = []
    for b in buckets:
        hashed = set(i[1] for i in buckets[b]) # unique hash values in bucket
        for h in hashed:
            shares_this_hash = [i[0] for i in buckets[b] if i[1] == h]
            if len(shares_this_hash) > 1:
                for p in itertools.product(shares_this_hash, shares_this_hash):
                    p0, p1 = p
                    if p0 != p1:
                        out.append((p0, p1)) if p0 < p1 else out.append((p1, p0))
    return set(out)



def run():
    print "[*] running on {} docs".format(NBILLS)

    V, docs = get_docs()

    D = len([f for f in glob.glob(PATHTOBILLS)])  # ndocs

    V = {w: kno for kno, w in enumerate(V)}

    print "[*] found a vocab of size {}".format(len(V))

    M = np.zeros((len(V), D), dtype=bool)

    # in real stuff, this is sparse
    for dno, d in enumerate(docs):
        for w in d:
            M[V[w]][dno] = 1

    print "[*] Filled M"

    hashes = [{k: generator.randint(0, len(V)) for k in range(len(V))} for i in range(n)]

    def fill_sig():
        SIG_ = np.empty((n, D))
        SIG_[:] = 1000000000

        for r in range(len(V)):
            if r % 100 == 0:
                sys.stderr.write("processes {} of {} words,\t".format(r, len(V)))
            for c in range(D):
                if M[r][c] == 1:
                    for i in range(n):
                        SIG_[i][c] = min(SIG_[i][c], hashes[i][r])

        return SIG_

    SIG = fill_sig()
    print "[*] dumping"
    with open("sig.p", "w") as ouf:
        pickle.dump(SIG, ouf)

    print "\n[*] Filling buckets"
    r = int(math.floor(SIG.shape[0] / bands))

    bucket_arrays = defaultdict(list)

    for i in range(0, SIG.shape[0], r):
        print i, SIG.shape[0]
        band_row_start = i
        band_row_end = min(i + r, SIG.shape[0])
        for c in range(SIG.shape[1]):
            band = " ".join([str(p) for p in SIG[:, c][band_row_start:band_row_end]])
            bucket_arrays[i].append((c, hashlib.md5(band).hexdigest()))

    print "\n[*] Filled buckets"
    with open("buckets.p", "w") as ouf:
        pickle.dump(bucket_arrays, ouf)
    print "\n[*] Dumped buckets"

def test_mode():
    iters = 200
    j = 0

    all_docs = [int(f.split("/")[1].replace(".txt", "")) for f in glob.glob("test_data/*txt")]

    to_check = []
    for p in itertools.product(all_docs, all_docs):
        a, b = p
        if a != b:
            to_check.append(p)

    matches = defaultdict(float)
    jaccards = defaultdict(float)
    for i in range(iters):
        print "iter,", i
        run()
        pairs = get_pairs()
        print len(to_check)
        for d1, d2 in to_check:
            # print d1
            matches[(d1, d2)] += len([p for p in pairs if d1 in p and d2 in p])
            jaccards[(d1, d2)] += estimated_jaccard(d1, d2)

    for check in to_check:
        plt.scatter(jaccards[check] / iters, matches[check] / iters, alpha=0.5)

    plt.show()

if __name__ == "__main__":
    run()
    # test_mode()
    pairs = get_pairs()
    with open("pairs.txt", "w") as outf:
        for p in pairs:
            outf.write("{},{}\n".format(p[0], p[1]))