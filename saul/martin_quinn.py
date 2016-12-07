import pandas as pd
import numpy as np
from linreg import linreg_post
from norm1d import *

# each vote by each legislator gets a z score, the utility from the vote
model_df = pd.DataFrame.from_csv("model_position_df.df")
model_df["z"] = np.random.uniform(-1,1, model_df.shape[0])

# legislators
leg = pd.DataFrame(model_df["legislator"].unique(), columns=["legislator"])
leg["theta"] = np.random.uniform(-1,1, leg.shape[0])

# votes
votes = pd.DataFrame(model_df["vote"].unique(), columns=["vote"])
votes["alpha"] =  np.random.uniform(-1,1, votes.shape[0])
votes["beta"] = np.random.uniform(-1,1, votes.shape[0])

ITERS = 200

def draw_z(row):
    """
    """
    voteinfo = votes.query("vote=={}".format(row["vote"]))
    theta = leg.query("legislator=={}".format(row["legislator"]))["theta"]
    theta_float = theta[theta.keys()[0]]   # this is a float! 
    leginfo = leg.query("legislator=={}".format(row["legislator"]))
    mean =  voteinfo["alpha"] + voteinfo["beta"] * theta_float
    mean_float = mean[mean.keys()[0]]
    standard_deviation = 1
    
    if row["position"] == 1:
        return truncnormal(mean_float, standard_deviation, 0, 100)
    elif row["position"] == 0:
        return truncnormal(mean_float, standard_deviation, -100, 0)
    assert "do not" == "get to here"

def draw_theta(row):
    """
    Draw a theta
    """
    ls_votes = model_df.query("legislator=={}".format(row["legislator"]))
    ls_votes = ls_votes.merge(votes, on='vote')
    X = ls_votes[["alpha", "beta"]].as_matrix()
    Y = ls_votes["z"].as_matrix()
    m, cv = linreg_post(X, Y, np.zeros(2), 1, 1)
    return np.random.multivariate_normal(m, cv)[1]


def draw_ab(row):
    """
    Draw a theta
    """
    vote_i = model_df.query("vote=={}".format(row["vote"]))
    vote_i = vote_i.merge(leg, on="legislator")
    vote_i["dummy"] = 1
    X = vote_i[["dummy", "theta"]].as_matrix()
    Y = vote_i["z"]
    m, cv = linreg_post(X, Y, np.zeros(2), 1, 1)
    a, b = np.random.multivariate_normal(m, cv)
    vote = row["vote"]
    return pd.Series([vote, a, b], index=['vote', 'alpha_new', 'beta_new'])

LOG_FILENAME = 'sampler.log'
import os
try:
    os.remove(LOG_FILENAME)
except:
    pass
    
import logging

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG, format='%(asctime)s\t %(message)s')


# clear old traces
import glob
for f in glob.glob("trace/*"):
    os.remove(f)

def likelihood(row):
    zscore = row["alpha"] + row["beta"] * row["theta"]
    # print row
    if row["position"] == 0:
        return np.log(normcdf(1 - zscore))
    elif row["position"] == 1:
        return np.log(normcdf(zscore))
    else:
        assert "bad" == "problem"


def ll():
    # is it good?
    t = model_df.merge(leg, on="legislator").merge(votes, on="vote")
    t["ll"] = t.apply(likelihood, axis=1)
    return np.sum(t["ll"])
    

for i in range(ITERS):
    logging.debug("{}\t{}".format(i, ll()))
    #z should go 1st or first iter is wasted
    model_df["z"] = model_df.apply(draw_z, axis=1)
    
    # alpha, beta
    new = votes.apply(draw_ab, axis=1)
    votes = votes.merge(new, on="vote")[["vote", "alpha_new", "beta_new"]]
    votes.columns = ["vote", "alpha", "beta"]
    
    #theta
    leg["theta"] = leg.apply(draw_theta, axis=1)

    leg.to_csv("trace/leg_{}".format(i))
    votes.to_csv("trace/votes_{}".format(i))
