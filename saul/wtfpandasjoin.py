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

with open("votes_merged.csv", "r") as inf:
    reader = csv.reader(inf)
    next(reader, None) # skip header
    for ln in reader:
        print ln
        congress = ln[1]
        number = int(float(ln[2]))
        btype = ln[3]
        ideology = ln[4]
        bill = Bill(number, btype, congress, ideology)
        print bill
        bills.append(bill)


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
            with open("pairs_enhanced_again.txt", "a") as outf:
                writer = csv.writer(outf)
                writer.writerow(ln + [ideology_a, ideology_b])
        except IndexError:
            ideology_a = "unknown"
            ideology_b = "unknown"
            with open("pairs_enhanced_again.txt", "a") as outf:
                writer = csv.writer(outf)
                writer.writerow(ln + [ideology_a, ideology_b])
