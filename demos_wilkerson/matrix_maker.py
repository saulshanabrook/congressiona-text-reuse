import glob
import numpy as np
from datetime import datetime
import re
import ipdb

files = glob.glob("*txt")

mo_mapper = {"oct": 10, "july": 7, "dec": 12, "june": 6, "mar": 3, "sep": 9}


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def vocab(input_dict):
    '''numberize'''
    fc = [v["5-gms"] for k,v in input_dict.items()]
    vocab_ = set(reduce(lambda x,y: x.union(y), fc))
    return {v:k for k,v in enumerate(vocab_)}


def get_ordered_dates():
    files_dates = []
    for fno, f in enumerate(files):
        mo = re.search("[a-z]+_[0-9]+_[0-9]+.txt", f).group()
        month = int(mo_mapper[mo.split("_")[0]])
        day = int(mo.split("_")[1])
        year = int(mo.split("_")[2].replace(".txt", ""))
        dt = datetime(year, month, day)
        files_dates.append((dt, f))
    files_dates.sort(key=lambda x:x[0])
    return [p[1] for p in files_dates]


def build_corpus():
    data = {}
    for fno, f in enumerate(get_ordered_dates()):
        with open(f, "r") as inf:
            txt = inf.read().split()
            mo = re.search("[a-z]+_[0-9]+_[0-9]+.txt", f).group()
            month = int(mo_mapper[mo.split("_")[0]])
            day = int(mo.split("_")[1])
            year = int(mo.split("_")[2].replace(".txt", ""))
            dt = datetime(year, month, day)
            ngrams = find_ngrams(txt, 5)
            data[fno] = {"date": dt.strftime("%Y-%m-%d"), "5-gms": set(ngrams)}
    return data

data = build_corpus()
V = vocab(data)

# 5-gm document matrix
mx = np.zeros((len(V), len(data)))

for doc, items in data.items():
    for fgm in items["5-gms"]:
        n = V[fgm]
        mx[n][doc] = 1

def name_note(time, txt):
    '''naming convention for nodes'''
    return "{}-{}".format(time, V[txt])

# represents a sparse matrix. Each tuple (i,j) means 5-gm i is parent of j
# you can imagine this as a big matrix: ndocs * |V| rows and cols
parents = []
for dno in range(2, len(data)):
    for fvgrm in data[dno]['5-gms']:
        if fvgrm in data[dno - 1]['5-gms']:
            parents.append((name_note(dno - 1, fvgrm), name_note(dno, fvgrm)))

print len(parents), len(V)
