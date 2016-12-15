'''
this script takes pairs_enhanced.txt from bills_sensemaker.py from the ulman dupefinder

- it adds ideologies to bills
- it outputs pairs_enhanced_again.txt

'''

import collections
import csv, ipdb, os
import ipdb
import json

Bill = collections.namedtuple('Bill', 'billno billtype congress ideology')




def remove_old_file_and_reset_stuff():
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

def get_bills():
    bills = []
    with open("votes_merged.csv", "r") as inf: # this is a CSV from sauls govtrack dfs
        reader = csv.reader(inf)
        next(reader, None) # skip header
        for ln in reader:
            print ln
            congress = int(ln[1])
            number = int(float(ln[2]))
            btype = ln[3]
            ideology = ln[4]
            bill = Bill(number, btype, congress, ideology)
            print bill
            bills.append(bill)
    return bills

def add_ideologyscores():
    with open("pairs_enhanced.txt", "r") as inf:
        reader = csv.reader(inf)
        next(reader, None) # skip header
        for ln in reader:
            try:
                # ipdb.set_trace()
                adt = json.loads(ln[2])
                ano, atype, acongress = int(adt["billno"]), adt["billkind"], int(adt["congress"])
                bdt = json.loads(ln[7])
                bno, btype, bcongress = int(bdt["billno"]), bdt["billkind"], int(bdt["congress"])
                billa = [a for a in bills if a.billno == ano and a.billtype==atype].pop()
                billb = [b for b in bills if b.billno == bno and b.billtype==btype].pop()
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


remove_old_file_and_reset_stuff()
add_ideologyscores()
