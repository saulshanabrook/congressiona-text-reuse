import glob
import json
from stanford_corenlp_pywrapper import CoreNLP


proc = CoreNLP("pos", corenlp_jars=["/Users/ahandler/stanford-corenlp-full-2015-04-20/*"])

for fn in glob.glob("demos_congress/*txt"):
    with open(fn, "r") as inf:
        procd = proc.parse_doc(inf.read())
        with open(fn.replace(".txt", ".anno"), "w") as outf:
            outf.write(json.dumps(procd))

for fn in glob.glob("demos/*txt"):
    with open(fn, "r") as inf:
        procd = proc.parse_doc(inf.read())
        with open(fn.replace(".txt", ".anno"), "w") as outf:
            outf.write(json.dumps(procd))

