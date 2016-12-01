'''
la la la i hate pandas (hitting error on join)
'''

import collections
import csv, ipdb

Bill = collections.namedtuple('Bill', 'billno billtype congress ideology')

bills = []

with open("vote_pt_df.csv", "r") as inf:
    reader = csv.reader(inf)
    next(reader, None) # skip header
    for ln in reader:
        congress = ln[5]
        number = ln[6]
        btype = ln[8]
        ideology = ln[28]
        bills.append(Bill(number, btype, congress, ideology))

with open("pairs_enhanced.txt", "r") as inf:
    reader = csv.reader(inf)
    for ln in reader:
        ano, atype, acongress = ln[2], ln[3], ln[4]
        bno, btype, bcongress = ln[9], ln[10], ln[11]
        print bno, btype, bcongress
#print pairs[0]
#print votept[0]