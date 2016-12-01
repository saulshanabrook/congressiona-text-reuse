'''
la la la i hate pandas (hitting error on join)
'''

import collections
import csv, ipdb, os

Bill = collections.namedtuple('Bill', 'billno billtype congress ideology')

bills = []

try:
    os.remove("pairs_enhanced_again.txt")
    with open("pairs_enhanced.txt", "r") as inf:
        reader = csv.reader(inf)
        header = reader.next() + ["ideology_a", "ideology_b"]
        with open("pairs_enhanced_again.txt", "a") as outf:
            writer = csv.writer(outf)
            writer.writerow(header)
except OSError:
    print "could not find"

with open("vote_pt_df.csv", "r") as inf:
    reader = csv.reader(inf)
    next(reader, None) # skip header
    for ln in reader:
        congress = ln[5]
        number = int(float(ln[6]))
        btype = ln[8]
        ideology = ln[28]
        bills.append(Bill(number, btype, congress, ideology))

with open("pairs_enhanced.txt", "r") as inf:
    reader = csv.reader(inf)
    next(reader, None) # skip header
    for ln in reader:
        try:
            ano, atype, acongress = int(ln[2]), ln[3], ln[4]
            bno, btype, bcongress = int(ln[9]), ln[10], ln[11]
            billa = [a for a in bills if a.billno == ano and a.billtype==atype].pop()
            billb = [b for b in bills if a.billno == bno and b.billtype==btype].pop()
            ideology_a = billa.ideology
            ideology_b = billb.ideology
        except IndexError:
            ideology_a = "unknown"
            ideology_b = "unknown"
        print ideology_a, ideology_b
        with open("pairs_enhanced_again.txt", "a") as outf:
            writer = csv.writer(outf)
            writer.writerow(ln + [ideology_a, ideology_b])
#print pairs[0]
#print votept[0]