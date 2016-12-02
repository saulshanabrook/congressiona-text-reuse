import glob
import json
from stanford_corenlp_pywrapper import CoreNLP


proc = CoreNLP("pos", corenlp_jars=["/Users/ahandler/stanford-corenlp-full-2015-04-20/*"])


locs = ["govtrackdata/108/*", "govtrackdata/109/*", "govtrackdata/110/*", "govtrackdata/111/*",  "govtrackdata/112/*",  "govtrackdata/113/*"] 

for loc in locs:
    for fn in glob.glob(loc):
        with open(fn, "r") as inf:
            procd = proc.parse_doc(inf.read())
            with open(fn.replace(".txt", ".anno"), "w") as outf:
                outf.write(json.dumps(procd))


