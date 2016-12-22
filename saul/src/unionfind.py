import numpy as np
import pandas as pd
import cPickle as pickle
from collections import defaultdict


def get_graph():
    G = np.zeros((5,5))
    for i in range(3):
        for j in range(3):
            G[i][j] = 1

    for i in range(3,5):
        for j in range(3,5):
            G[i][j] = 1
    return G


def connected_components(G):
    '''CLRS chapter 21 but w/ python dicts'''
    sets = dict()

    for vno, v in enumerate(G):
        sets[vno] = vno  # MakeSet
        
    it = np.nditer(G, flags=['multi_index'])
    last = 0
    while not it.finished: # for each edge in graph
        if last != it.multi_index[0]: # just some printout updates
            print it.multi_index[0]
            last = it.multi_index[0]
        if it[0] == 1.0:
            u, v = it.multi_index
            if sets[u] != sets[v]:
                sets[u] = sets[v]
        it.iternext()
    # sets is a dictionary saying what set a vertex is in
    out = defaultdict(list)
    for s in sets.keys():
        out[sets[s]].append(s)
    return out


def get_df():
    reuse = pd.DataFrame.from_csv("pairs_enhanced_again.txt") #.head()
    reuse["ideology"] = reuse["jac"].astype(float)
    reuse = reuse[reuse["jac"] > .8]
    return reuse

def get_guids(reuse):
    guids = reuse["b_section_guid"].append(reuse["a_section_guid"]).unique()
    guid_dic = {k: guid for k, guid in enumerate(guids)}
    guid_dic_r = {guid: k for k, guid in enumerate(guids)}
    return guid_dic, guid_dic_r
    
def make_reuse_graph():
    reuse = get_df()
    guid_dic, guid_dic_r = get_guids(reuse)
    G = np.zeros((len(guid_dic), len(guid_dic)))
    def fill_v(row):
        G[guid_dic_r[row["a_section_guid"]]][guid_dic_r[row["b_section_guid"]]] = 1
        G[guid_dic_r[row["b_section_guid"]]][guid_dic_r[row["a_section_guid"]]] = 1
    reuse.apply(fill_v, axis=1)
    return G

g = make_reuse_graph()
sets = connected_components(g)
with open("sets.p", "w") as outf:
    pickle.dump(sets, outf)