import itertools
import pathlib
import pandas as pd
import tqdm
import json
import numpy as np


def legislators():
    """
    Returns a dataframe of all legislators.

    Each row contain at least the senators roll call ID "bioguide_id"
    """

    return pd.concat(map(pd.read_csv, [
        "../govtrackdata/congress-legislators/legislators-current.csv",
        "../govtrackdata/congress-legislators/legislators-historic.csv"
    ]), ignore_index=True)


def _transform_dict_items(d, join_string="_"):
    """
    Transforms the dictionary d to remove the values which
    are dictionaries and add each key of that dictionary
    as the original key appended with that key.
    
        _transform_dict_items({
            "hi": 1,
            "there": {"inner": 2}
        }) === {"hi": 1, "there_inner": 2}
    """
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                new_dict["{}{}{}".format(k, join_string, k2)] = v2
        else:
            new_dict[k] = v
    return new_dict

def _load_json(path):
    with open(str(path)) as f:
        return json.load(f)

def bills(legislator_df):
    """
    Returns two dataframes:

    bill_df:
        rows: one for each bill
        columns: 
    sponsor_df:
        rows: each sponsor/cosponsor on eacn bill
        columns: [is_cosponsor (True, False), bill_index, legislator_index]
    """
    thomas_id_to_index  = {int(label): index for (index, label) in legislator_df['thomas_id'].items() if not np.isnan(label)}
    bills = []
    sponsors = []
    for bill_index, bill in enumerate(map(_load_json, tqdm.tqdm_notebook(_bill_paths(), desc="bills"))):
        bills.append(bill)

        sponsor = bill.pop('sponsor')
        sponsors.append({
            "is_cosponsor": False,
            "bill_index": bill_index,
            "legislator_index": thomas_id_to_index[int(sponsor['thomas_id'])]
        })
        for cosponsor in  bill.pop('cosponsors'):
            sponsors.append({
                "is_cosponsor": True,
                "bill_index": bill_index,
                "legislator_index": thomas_id_to_index[int(cosponsor['thomas_id'])]
            })

    return pd.DataFrame.from_records(bills), pd.DataFrame.from_records(sponsors)


def _bill_paths():
    return list(pathlib.Path("../govtrackdata/").glob("congress/*/bills/*/*/data.json"))

def votes(legislator_df, bill_df):
    """
    Returns two dataframes: (vote_df, position_df)

    vote_df:
        rows: one for each roll call/vote
        columns: [date, category, bill_index, ...others]
    position_df
        rows:  each legislators position on the vote
        columns: [vote_index, legislator_index, position ("Aye", "No", "Present", ...)]
    """
    roll_call_id_to_index = _build_legislator_name_to_index(legislator_df)
    bill_id_to_index  = {label: index for (index, label) in bill_df['bill_id'].items()}

    votes = []
    positions = []
    for vote_index, vote in enumerate(map(_load_json, tqdm.tqdm_notebook(_vote_paths(), desc="votes"))):
        votes.append(vote)

        bill = vote.pop("bill", None)
        if bill:
            bill_id = "{type}{number}-{congress}".format(**bill)
            vote['bill_index'] = bill_id_to_index[bill_id]

        for position, legislators in vote.pop("votes").items():
            for legislator in legislators:
                positions.append({
                    "position": position,
                    "vote_index": vote_index,
                    "legislator_index": roll_call_id_to_index[legislator["id"]],
                })
    return pd.DataFrame.from_records(votes), pd.DataFrame.from_records(positions)


def _vote_paths():
  return list(pathlib.Path("../govtrackdata/").glob("congress/*/votes/**/data.json"))


def _build_legislator_name_to_index(legislator_df):
    """
    Returns a dictionary mapping each legislator ID (both their bioguide_id and their lis_id) to the index
    of the legislator in the dataframe
    """
    return {label: index for (index, label) in itertools.chain(
        legislator_df['bioguide_id'].items(),
        legislator_df['lis_id'].items()
    )}
