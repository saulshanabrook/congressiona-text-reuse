## Prelim stuff
# python makedemos.py

## Real stuff

#THIS DOES NOT WORK W/O LC_ALL=C 
#http://man7.org/linux/man-pages/man1/sort.1.html


echo "[*] shingling"

#FILES="/data/bills/mdenny_copy_early2015/bills/*anno"
#FILES="/data/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/*anno"
for (( c=0; c<100; c++ ))
do
    python pi.py
    find /data/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/ -type f -name '*.anno' | parallel --eta -j20 python shingling.py -doc {} -iter "$c"
done


# echo "[*] sorting"
LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted
python build_sketches.py shingles.congress.sorted

# rm supershingles.txt
# find sketches -type f | parallel -j 4 python supershingle.py {}
# LC_ALL=C sort -k2 -n -t"," supershingles.txt > supershingles.sorted
# py supershingle_reader.py | sort | uniq  | wc -l  # 14

python reducer.py

awk -F, '{print >> ("pairs/"$2".csv"); close("pairs/"$2".csv")}' shingles.congress.sorted.filter

# get the jaccard
./sketch_nums.sh sketches/demos_congress#hr_201.anno_4 sketches/demos_congress#hr_202.anno_4

echo "[*] finding jaccards"
rm shingles.congress.candidates.jacs


sort shingles.congress.candidates | uniq > t
mv t shingles.congress.candidates

# cat shingles.congress.candidates | parallel python check_candidate.py {}


