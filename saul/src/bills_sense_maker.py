# this gets run after ulman.py
from __future__ import division
from ulman import get_tokens, jaccard
import ujson as json
import glob, csv, os, ipdb, re
PATHTOBILLS = "sections/*anno"

def get_dmapper():
    '''get all anno files in PATHTOBILLS'''
    d = {}
    for fno, f in enumerate(glob.glob(PATHTOBILLS)):
        d[fno] = f
    return d


def decode_bill_id(inln, request):
    billno_type, congress, billcode = inln.split("-")
    billno = re.search("[0-9]+", billno_type).group(0)
    billkind = billno_type.replace(billno, "") #hr, hres, etc. 
    if request == "billno":
        return billno
    elif request == "billkind":
        return billkind
    elif request == "congress":
        return congress


try:
    os.remove("pairs_enhanced.txt")
    with open("pairs_enhanced.txt", "a") as outf:
        writer = csv.writer(outf, quoting=csv.QUOTE_NONNUMERIC)
        header = ["afn", "a_section_guid", "bill_no_a", "bill_kind_a", "congress_a", "version_code_a", "issued_on_a", "bfn", "b_section_guid",  "bill_no_b", "bill_kind_b", "congress_b", "version_code_b", "issued_on_b", "jac"]
        writer.writerow(header)
    print "removed"
except OSError:
    print "could not find"

mapper = get_dmapper()

BASE = ""

with open("pairs.txt", "r") as inf:
    for lno, ln in enumerate(inf):
        if lno % 10000 == 0:
            print lno
        a, b = [mapper[int(r)] for r in ln.replace("\n", "").split(",")]
        with open(BASE + a.split("_._")[1].replace("_", "/").replace("document.anno", "") + "data.json", "r") as inf:
            real_a = json.load(inf)
        with open(BASE + b.split("_._")[1].replace("_", "/").replace("document.anno", "") + "data.json", "r") as inf:
            real_b = json.load(inf)
        tok_a = get_tokens(a) # needed for Jac
        tok_b = get_tokens(b)
        section_no_a =  a.replace("/Users/ahandler/PycharmProjects/ulman/govtrak/sections/", "").split("_._")[0]
        section_no_b =  b.replace("/Users/ahandler/PycharmProjects/ulman/govtrak/sections/", "").split("_._")[0]
        bsection_guid = b.split("_._")[0].split("/").pop()
        asection_guid = a.split("_._")[0].split("/").pop()

        try:
            jac = len(set(tok_a).intersection(set(tok_b))) / len(set(tok_a).union(set(tok_b)))
        except ZeroDivisionError:
            pass
        with open("pairs_enhanced.txt", "a") as outf:
            writer = csv.writer(outf, quoting=csv.QUOTE_NONNUMERIC)

            # I think issued_on means date the bill was introduced. NOT voted. 
            # See... https://www.congress.gov/bill/113th-congress/house-bill/2821 and 
            # /Users/ahandler/PycharmProjects/ulman/govtrak/bills/hr/hr2821/text-versions/ih/data.json
            writer.writerow([a, asection_guid, 
                             decode_bill_id(real_a["bill_version_id"], "billno"),
                             decode_bill_id(real_a["bill_version_id"], "billkind"),
                             decode_bill_id(real_a["bill_version_id"], "congress"),
                             real_a["version_code"], real_a["issued_on"],
                             b, bsection_guid,
                             decode_bill_id(real_b["bill_version_id"], "billno"),
                             decode_bill_id(real_b["bill_version_id"], "billkind"),
                             decode_bill_id(real_b["bill_version_id"], "congress"),
                             real_b["version_code"],
                             real_b["issued_on"], jac])



