import itertools
import pathlib
import pandas as pd
import tqdm
import json


def legislators():
    """
    Returns a dataframe of all legislators.

    Each row contain at least the senators roll call ID "bioguide_id"
    """

    return pd.concat(map(pd.read_csv, [
        "govtrackdata/congress-legislators/legislators-current.csv",
        "govtrackdata/congress-legislators/legislators-historic.csv"
    ]), ignore_index=True)



def votes(legislator_df):
    """
    Returns two dataframes: (vote_df, vote_position_df)

    vote_df:
        rows: one for each roll call/vote
        columns: [date, category, ...others]
    position_df
        rows:  each legislators position on the vote
        columns: [vote_index, legislator_index, position ("Aye", "No", "Present", ...)]
    """
    roll_call_id_to_index = _build_legislator_name_to_index(legislator_df)
    votes = []
    vote_positions = []
    for vote_index, path in enumerate(tqdm.tqdm_notebook(_vote_paths())):
        with open(str(path)) as f:
            vote = json.load(f)
            votes.append(vote)
            for position, legislators in vote.pop("votes").items():
                for legislator in legislators:
                    vote_positions.append({
                        "position": position,
                        "vote_index": vote_index,
                        "legislator_index": roll_call_id_to_index[legislator["id"]],
                    })
    return pd.DataFrame.from_records(votes), pd.DataFrame.from_records(vote_positions)


def _vote_paths():
  return list(pathlib.Path("./govtrackdata/").glob("**/votes/**/data.json"))


def _build_legislator_name_to_index(legislator_df):
    """
    Returns a dictionary mapping each legislator ID (both their bioguide_id and their lis_id) to the index
    of the legislator in the dataframe
    """
    return {label: index for (index, label) in itertools.chain(
        legislator_df['bioguide_id'].items(),
        legislator_df['lis_id'].items()
    )}