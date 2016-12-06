import pandas as pd
import numpy as np
import ipdb
from norm1d import normcdf

position = pd.DataFrame.from_csv("position.df")
position = position[position["position"].str.contains("Aye|Nay")] # limit to Aye/Nay votes
LEG = set(position["legislator_index"].unique())
VOTES = set(position["vote_index"].unique())
NLEG = len(LEG)
NVOTES = len(VOTES)

# print NLEG, NVOTES

## initalize

PRIOR_VARIANCE = 1
EMISSION_SCALAR = 1

def get_matrixes():
    out = np.zeros((NLEG, NVOTES))
    for i in xrange(NLEG):
        out[i] = np.asarray(np.random.normal(0,1,NVOTES))
    return out

leg_counter = {v:k for k,v in enumerate(LEG)}
vote_counter = {v:k for k,v in enumerate(VOTES)}
thetas = np.asarray(np.random.normal(0,1,NLEG))
alphas = np.asarray(np.random.normal(0,1,NVOTES))
betas = np.asarray(np.random.normal(0,1,NVOTES))
Zs = get_matrixes()

PRIOR_MEAN = np.zeros(2)
THETA_PRIOR_MEAN = np.asarray([0])

B0 = np.zeros((2,2))
np.fill_diagonal(B0, PRIOR_VARIANCE)


def lookup_vote(legislator_index, vote_index):
    """
    Lookup vote
    """
    ix = position.query("legislator_index=={} & vote_index=={}".format(legislator_index, vote_index)).index[0]
    if position["position"][ix] == "Nay":
        return 0
    else:
        return 1

def voted_on(legislator_index):
    """
    Get all votes for justice, j
    """
    return position_df.query("legislator_index=={}".format(legislator_index))


def alpha_for(vec_k):
    out = np.zeros(len(vec_k))
    for k in vec_k:
        out[k] = alphas[k]
    return out


def betas_for(vec_k):
    out = np.zeros(len(vec_k))
    for k in vec_k:
        out[k] = betas[k]
    return out


def draw_z(k, j):
    """
    draw a z for case k, justice j

    eq. 9 from the paper 

    TODO: omitting noise b/c they don't include noise
    """
    vote = lookup_vote(k, j)
    mean = alphas[k] + (betas[k] * thetas[j])
    #print mean, vote
    assert vote in [0, 1]
    standard_deviation = 1
    if vote == 1:
        return truncnormal(mean, standard_deviation, 0, 100)
    elif vote == 0:
        return truncnormal(mean, standard_deviation, -100, 0)

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
    ab = np.asarray([(alphas[i], betas[i]) for i in voted_on(j)])
    z = np.asarray([Zs[j][k] for k in voted_on(j)])
    for iit in voted_on(j):
        zz = Zs[j][k]
        if zz == 0.0:
            ipdb.set_trace()
    vw, v0 = linreg_post(ab, z, np.zeros(ab.shape[1]), 1, 1)
    out = np.random.multivariate_normal(vw, v0)
    return out[1]
    #out = np.random.normal(vw, v0)
    #return out

def resample_theta():
    for j_ix, theta in enumerate(thetas):
        thetas[j_ix] = draw_theta(j_ix)

def resample_alphabeta():
    for k_ix in range(len(alphas)):
        # indexes of judges who voted on case, k
        jk = [j for j, v in enumerate(votes[k_ix]) if v != -9]
        a, b = draw_ab(k_ix, thetas, Zs, jk)
        alphas[k_ix] = a
        betas[k_ix] = b


def resample_Z():
    for j, zl in enumerate(Zs):
        for k, z in enumerate(zl):
            assert j < Njus
            try:
                Zs[j][k] = draw_z(k, j)
            except AssertionError:
                #print "s"
                Zs[j][k] = 0 # pass


def ll_simple():
    sump = 0
    for index, row in position.iterrows():
        if index % 1000 == 0:
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
    ## Run the sampler and save a copy of the variables at each iteration.
    samples = []
    for siter in xrange(1000):
        print siter
        ll = ll_simple()
        print ll
        resample_Z()
        print "resampled z"
        resample_theta()
        print "resampled theta"
        resample_alphabeta()
        print "resampled AB"
        samples.append({'theta':thetas.copy(), 'll': ll, 'alpha':alphas.copy(), 'beta':betas.copy()})
    import pickle as pickle
    pickle.dump(samples, open("samples.p", "w"))
    ## Not saving Z since it can take a lot of memory.  1000 iters is ok, but 10000 iters is >1 GB (since it takes up 10000*Njus*Ncase*8 or so bytes.)


sampler()