import pandas as pd
import numpy as np
import ipdb
from norm1d import *

position = pd.DataFrame.from_csv("position.df")
position = position[position["position"].str.contains("Aye|Nay")] # limit to Aye/Nay votes
position['z'] = np.random.uniform(-1,1, position.shape[0]) # init some random utilites

leg = pd.DataFrame(position["legislator_index"].unique(), columns=["legislator_index"])
leg["theta"] = np.random.uniform(-1,1, leg.shape[0]) # init some random thetas

bills = pd.DataFrame(position["vote_index"].unique(), columns=["vote_index"])
bills["alpha"] = np.random.uniform(-1,1, bills.shape[0])
bills["beta"] = np.random.uniform(-1,1, bills.shape[0]) 

print bills.head()
## initalize

PRIOR_VARIANCE = 1
EMISSION_SCALAR = 1

PRIOR_MEAN = np.zeros(2)
THETA_PRIOR_MEAN = np.asarray([0])

B0 = np.zeros((2,2))
np.fill_diagonal(B0, PRIOR_VARIANCE)


def lookup_vote(legislator_index, vote_index):
    """
    Lookup vote
    """
    print legislator_index, vote_index, type(legislator_index)
    ipdb.set_trace()
    ix = position.query("legislator_index=={} & vote_index=={}".format(legislator_index, vote_index)).index[0]
    return position["position"][ix]


def draw_z(row):
    """
    """
    ipdb.set_trace()
    try:
        legislator_index = row["legislator_index"]
        vote_index = row["vote_index"]
    except KeyError:
        return 0
    billinfo = row.merge(bills, on=("vote_index"))
    leginfo = row.merge(leg, on=("legislator_index"))
    assert len(billinfo.index) == 1
    assert len(leginfo.index) == 1
    mean =  billinfo.loc[0]["alpha"] + billinfo.loc[0]["beta"] * leginfo.loc[0]["theta"]
    standard_deviation = 1
    if row.loc[row.index.values[0]]["position"] == "Aye":
        return truncnormal(mean, standard_deviation, 0, 100)
    elif row.loc[row.index.values[0]]["position"] == "Nay":
        return truncnormal(mean, standard_deviation, -100, 0)
        assert "do not" == "get to here"

def draw_ab(k, thetas_, Zs_, jk):
    """
    Draw a alpha beta based on the eq 10 in Martin + Quinn
    """

    THETAJCONST = 1

    def theta_j(j):
        out = np.zeros((2, 1))
        out[0][0] = THETAJCONST
        out[1][0] = thetas_[j]
        return np.transpose(out)

    def get_theta(jk):
        mxs = [theta_j(j) for j in jk]
        return np.concatenate(mxs, axis=0)
    
    x = get_theta(jk)

    z = [Zs_[j][k] for j in jk]

    E = inv(np.dot(np.transpose(x), x) + inv(B0))
    e = np.dot(E, np.dot(np.transpose(x), z) + (np.dot(inv(B0), PRIOR_MEAN)))
    eta = np.random.multivariate_normal(e, E, 1)[0]
    return eta[0], eta[1]


def draw_theta(j):
    """
    Draw a theta
    """
    #ab = np.asarray([(alphas[i], betas[i]) for i in voted_on(j)])
    #z = np.asarray([Zs[j][k] for k in voted_on(j)])
    ipdb.set_trace()
    try:
        votedon = position.query("legislator_index=={}".format(j["legislator_index"]))
    except KeyError:
        return 0
    ipdb.set_trace()
    for iit in voted_on(j):
        zz = Zs[j][k]
        if zz == 0.0:
            ipdb.set_trace()
    vw, v0 = linreg_post(ab, z, np.zeros(ab.shape[1]), 1, 1)
    out = np.random.multivariate_normal(vw, v0)
    return out[1]


def resample_alphabeta():
    for k_ix in range(len(alphas)):
        # indexes of judges who voted on case, k
        jk = [j for j, v in enumerate(votes[k_ix]) if v != -9]
        a, b = draw_ab(k_ix, thetas, Zs, jk)
        alphas[k_ix] = a
        betas[k_ix] = b


def ll_simple():
    sump = 0
    for index, row in position.iterrows():
        if index % 10000 == 0:
            print index
        ak = alphas[vote_counter[row["vote_index"]]]
        bk = betas[vote_counter[row["vote_index"]]]
        tk = thetas[leg_counter[row["legislator_index"]]]
        zpx = ak + bk * tk
        v = lookup_vote(row["legislator_index"], row["vote_index"])
        if v == 0:
            sump += np.log(normcdf(1 - zpx))
        elif v == 1:
            sump += np.log(normcdf(zpx))
    return sump
    

def sampler():
    '''run sampler'''
    samples = []
    for siter in xrange(1000):
        print "iter", siter
        print position["z"].sum()
        # TODO delete
        # position["t"] = position.apply(draw_z) THIS DOES NOT WORK. 
        for index, row in position.iterrows():
            position.set_value(row["legislator_index"], row["vote_index"], draw_z(row))
            print position["z"].sum()
        print "resampled z"
        leg["theta"] = leg.apply(draw_theta)
        print "resampled theta"
        resample_alphabeta()
        print "resampled AB"
        samples.append({'theta':thetas.copy(), 'll': ll, 'alpha':alphas.copy(), 'beta':betas.copy()})
        print "calc ll"
        ll = ll_simple()
        print ll
    import pickle as pickle
    pickle.dump(samples, open("samples.p", "w"))

def test():
    '''debugger method'''
    print draw_z(position.iloc[[0]])

# test()
sampler()