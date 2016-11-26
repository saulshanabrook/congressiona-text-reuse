import pandas as pd
import pymc3 as pm
import pickle


def transform_data(position_df, vote_df, legislator_df):
    """
    Takes raw vote, position, and legislator data and returned cleaned data
    for modeling. It is limited to positions of yes/no and votes on documents.

    Returns a df `model_position_df` and two series `model_legislator_index`, `model_vote_index`

    The `model_position_df` lists all the actual roll call votes. Each vote position
    has a legislator and a vote. These are indexed from 0 to the number of legislators and votes
    respectively.

    The `model_legislator_index_df` and `model_vote_index_df` series map these
    indexes to the indexes in the vote_df and legislator_df dataframes.

    model_position_df:
        index: irrelevent
        columns:
            legislator: model index of legislator
            vote: model index of vote
            position: 1 if yes, 0 if no

    model_legislator_index:
        index: model index of legislator
        value: index of legislator in legislator_df

    model_vote_index:
        index: model index of vote
        value: index of vote in vote_df
    """
    POSITIONS = {
        "Yea": 1,
        "Aye": 1,
        "No": 0,
        "Nay": 0,
    }

    # only include vote positions with y/n positions
    position_df = position_df[position_df["position"].isin(POSITIONS.keys())] \
    # and only for position with bills
    position_df = position_df[list(vote_df.loc[position_df['vote_index']]['bill'].notnull())]

    legislator_index = list(set(position_df['legislator_index']))
    vote_index = list(set(position_df['vote_index']))

    model_legislator_index = pd.Series(legislator_index)
    model_vote_index = pd.Series(vote_index)

    model_legislator_index_inv = pd.Series(model_legislator_index.index, index=legislator_index)
    model_vote_index_inv = pd.Series(model_vote_index.index, index=vote_index)


    return pd.DataFrame({
        "position": list(position_df["position"].replace(POSITIONS)),
        "vote": list(model_vote_index_inv[position_df["vote_index"]]),
        "legislator": list(model_legislator_index_inv[position_df["legislator_index"]]),
    }), model_legislator_index, model_vote_index


def test_data(n_legislators):
    """
    Produce test data for modeling (`model_vote_position_df`).

    Assumes the legislator's positions go form -1 to 1.

    For example, for n=5 returns:

        pd.DataFrame({
            "legislator": [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4],
            "position":   [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
            "vote":       [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
        })
    """
    positions = []
    votes = []
    legislators = []
    for i in range(n_legislators - 1):
        positions.extend([1 if j <= i else 0 for j in range(n_legislators)])
        votes.extend([i for _ in range(n_legislators)])
        legislators.extend(range(n_legislators))
    return pd.DataFrame({
        "position": positions,
        "vote": votes,
        "legislator": legislators,
    })


def create_model(model_position_df):
    """
    Creates a PyMC3 Model for ideal point estimation
    using the IDEAL method based on
    "Comparing NOMINATE and IDEAL: Points of Difference and Monte Carlo Tests"
    """
    n_legislators = model_position_df['legislator'].nunique()
    n_votes = model_position_df['vote'].nunique()

    model = pm.Model()
    with model:
        leg_pt = pm.Normal("leg_pt", shape=n_legislators)
        a_0 = pm.Normal("a_0",  shape=n_votes)
        a_1 = pm.Normal("a_1", shape=n_votes)
        vote_pt = pm.Deterministic("vote_pt", -a_0 / a_1)

        position_leg_pt = leg_pt[model_position_df["legislator"]]
        position_a_0 = a_0[model_position_df["vote"]]
        position_a_1 = a_1[model_position_df["vote"]]

        p_position_yes = pm.invlogit(position_a_0 + position_leg_pt * position_a_1)
        position = pm.Bernoulli("position", p_position_yes, observed=model_position_df['position'])

    return model


def advi_params(model):
    """
    Estimate the parameters for the model, returns `advi_params`.
    """
    with model:
        return pm.variational.advi(n=25000)

def save_advi_params(advi_params):
    with open('advi_params.pickle', 'wb') as f:
        pickle.dump(advi_params, f)

def load_advi_params():
    with open('advi_params.pickle', 'rb') as f:
        return pickle.load(f)


def leg_add_ideal_pt(legislator_df, model_legislator_index, advi_params):
    """
    Adds the ideal points to the `legislators_df` and drops rows that don't
    have points.
    """
    return legislator_df.assign(
        ideal_pt=pd.Series(advi_params.means['leg_pt'], index=model_legislator_index)
    ).dropna(subset=['ideal_pt'])


def vote_add_ideal_pt(vote_df, model_vote_index, advi_params):
    """
    Adds the ideal points to the `votes_df` and drops rows that don't
    have points.
    """
    return vote_df.assign(
        ideal_pt=pd.Series(-advi_params.means['a_0'] / advi_params.means['a_1'], index=model_vote_index)
    ).dropna(subset=['ideal_pt'])

