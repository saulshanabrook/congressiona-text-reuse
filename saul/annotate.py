import glob
import json
from stanford_corenlp_pywrapper import CoreNLP


proc = CoreNLP("pos", corenlp_jars=["/Users/ahandler/stanford-corenlp-full-2015-04-20/*"])


locs = ["sections/*"] #, "test_data/*txt", "/Users/ahandler/Downloads/BILLS-113-1-hr/*_*txt"]


for loc in locs:
    for fn in glob.glob(loc):
        with open(fn, "r") as inf:
            procd = proc.parse_doc(inf.read())
            with open(fn.replace(".txt", ".anno"), "w") as outf:
                outf.write(json.dumps(procd))


