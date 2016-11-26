from __future__ import division
import pandas as pd
import numpy as np

df = pd.read_csv("shingles.congress")
aa = df[df["fn"] == "demos/1.anno"]
bb = df[df["fn"] == "demos/2.anno"]
print pd.merge(aa, bb, on='digit', how='inner').count(axis=0)

d1 = "the cat on the fence".split()
d2 = "the cat in the hat".split()

print len(set(d1).intersection(set(d2))) / len(set(d1).union(set(d2)))