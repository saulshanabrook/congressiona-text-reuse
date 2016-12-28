import csv
import json
import collections
import functools

# maps billinfo string to dict of version_code mapping to [issued_on, set of sectiosn guids]
bills = collections.defaultdict(functools.partial(collections.defaultdict, lambda: [None, set()]))

# list of (section guid 1, section guid 2, jacccard similarity)
overlaps = []

with open("data/reuse_df_no_unk.csv") as f:
    for row in csv.DictReader(f):

        for n in ('a', 'b'):
            bill = bills[row[f'billinfo_{n}']][row[f'version_code_{n}']]
            bill[0] = row[f'issued_on_{n}']
            bill[1].add(row[f'{n}_section_guid'])
        overlaps.append([
            row['a_section_guid'],
            row['b_section_guid'],
            float(row['jac'])
        ])


# from http://stackoverflow.com/a/8230505/907060
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super().default(self, obj)
 

with open("data/reuse.json", "w") as f:
    json.dump({
        "bills": bills,
        "overlaps": overlaps
    }, f, cls=SetEncoder)
