import glob
import json
from stanford_corenlp_pywrapper import CoreNLP


proc = CoreNLP("pos", corenlp_jars=["/home/sw/corenlp/stanford-corenlp-full-2015-04-20/*"])


locs = ["govtrackdata/108/sections/*", "govtrackdata/109/sections/*", "govtrackdata/110/sections/*", "govtrackdata/111/sections/*",  "govtrackdata/112/sections/*",  "govtrackdata/113/sections/*"] 

for loc in locs:
    for fn in glob.glob(loc):
        with open(fn, "r") as inf:
            procd = proc.parse_doc(inf.read())
            with open(fn.replace(".txt", ".anno"), "w") as outf:
                outf.write(json.dumps(procd))


