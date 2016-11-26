from __future__ import division
from collections import defaultdict
import numpy as np
import math
import hashlib
import random
import string
import glob

SEED = 5
generator = random.Random()
generator.seed(SEED)

n = 100 # permutations

def jaccard(a, b):
    return len(set(a).intersection(set(b)))/len(set(a).union(set(b)))
    
def get_docs():
    d1 = ["a", "b", "c", "d"]
    d2 = ["a", "c"]
    d3 = ["5", "2", "8", "9"] + [o for o in string.punctuation]
    d4 = ["5"]
    return [d1, d2, d3, d4]

docs = get_docs()
D = len(docs) # ndocs

V = {w:kno for kno, w in enumerate(set(reduce(lambda a,b: a+b, docs)))}

M = np.zeros((len(V), D))

# in real stuff, this is sparse
for dno, d in enumerate(docs):
    for w in d:
        M[V[w]][dno] = 1

hashes = [{k: generator.randint(0, len(V)) for k in range(len(V))} for i in range(n)]

SIG = np.empty((n,D,))
SIG[:] = 1000000000

for r in range(len(V)):
    for c in range(D):
        if M[r][c] == 1:
            for i in range(n):
                SIG[i][c] = min(SIG[i][c], hashes[i][r])


print "Sanity check"
print jaccard(d1, d2), "=?", len(set(SIG[:,0]).intersection(set(SIG[:,1])))/len(set(SIG[:,0]).union(set(SIG[:,1])))

bands = 50
bandsize = int(math.floor(SIG.shape[0]/bands))
bucket_arrays = defaultdict(list)

for i in range(0, SIG.shape[0], bandsize):
    band_row_start = i
    band_row_end = min(i + bandsize, SIG.shape[0])
    for c in range(SIG.shape[1]):
        band = " ".join([str(p) for p in SIG[:,c][band_row_start:band_row_end]])
        bucket_arrays[i].append((c, hashlib.md5(band).hexdigest()))

for ky in bucket_arrays.keys():
    print [o[1] for o in bucket_arrays[ky]][2] == [o[1] for o in bucket_arrays[ky]][3]