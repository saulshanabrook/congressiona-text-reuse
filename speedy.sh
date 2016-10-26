# bag of shingling heursitics. this is one iter

rm shingles.congress.candidates
rm shingles.congress
rm shingles.congress.sorted.filter

python pi.py
find demos_wilkerson -type f -name '*.anno' | parallel --eta -j20 python shingling.py -doc {} -iter NA
#done
LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted
python reducer.py shingles.congress.sorted
rsync -a --delete empty/ pairs/
cat shingles.congress.sorted.filter | pv | awk -F, '{print >> ("pairs/"$2".csv"); close("pairs/"$2".csv")}' shingles.congress.sorted.filter

# this yields a 10 fold reduction on pairs for wilkerson. from 7000k to 600
find pairs -type f | parallel --eta -j 2 ./pair_reducer.sh {}

# 
find pairs -type f | parallel --eta -j 2 python pairs_que_maker.py {}