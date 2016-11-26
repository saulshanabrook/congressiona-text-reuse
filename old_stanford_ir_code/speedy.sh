# bag of shingling heursitics. this is one iter

rm shingles.congress
rm shingles.congress.sorted.filter


python pi.py # generate permuatation

# shingle
find demos_wilkerson -type f -name '*.anno' | parallel --eta -j20 python shingling.py -doc {} -iter NA

# sort
LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted

# remove all shingles w/ no overlaps at all
python reducer.py shingles.congress.sorted

# delete the old pairs
rsync -a --delete empty/ pairs/

# break up pairs
cat shingles.congress.sorted.filter | pv | awk -F, '{print >> ("pairs/"$2".csv"); close("pairs/"$2".csv")}' shingles.congress.sorted.filter

# remove invalid pairs from same file
# this yields a 10 fold reduction on pairs for wilkerson. from 7000k to 600
find pairs -type f | parallel --eta -j 2 ./pair_reducer.sh {}

# DO NOT DELETE shingles.congress.candidates. this is the ag file
find pairs -type f | parallel --eta -j 2 python pairs_que_maker.py {}