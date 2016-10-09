import pandas as pd
import numpy as np

df = pd.read_csv("shingles.congress")
aa = df[df["fn"] == "demos/1.anno"]
bb = df[df["fn"] == "demos/2.anno"]
print pd.merge(aa, bb, on='digit', how='inner').count(axis=0)