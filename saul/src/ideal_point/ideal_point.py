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
    position_df = position_df[list(vote_df.loc[position_df['vote_index']]['bill_index'].notnull())]

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


def save_params(params):
    with open('../outputdata/params.pickle', 'wb') as f:
        pickle.dump(params, f)

def load_params():
    with open('../outputdata/params.pickle', 'rb') as f:
        return pickle.load(f)


def leg_add_ideology(legislator_df, model_legislator_index, params):
    """
    Adds the ideology to the `legislators_df` and drops rows that don't
    have values.
    """
    return legislator_df.assign(
        ideology=pd.Series(params['legislator_ideologies'], index=model_legislator_index)
    ).dropna(subset=['ideology'])


def vote_add_ideology_and_bias(vote_df, model_vote_index, params):
    """
    Adds the ideology and spread to the `votes_df` and drops rows that don't
    have values.
    """
    return vote_df.assign(
        ideology=pd.Series(params['vote_ideologies'], index=model_vote_index),
        bias=pd.Series(params['vote_biases'], index=model_vote_index)
    ).dropna(subset=['ideology'])

