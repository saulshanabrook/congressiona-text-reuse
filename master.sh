## Prelim stuff
# python makedemos.py

## Real stuff

#THIS DOES NOT WORK W/O LC_ALL=C 
#http://man7.org/linux/man-pages/man1/sort.1.html

echo "fn,digit,window_no,window_size,iter" > "shingles.congress"

echo "[*] shingling"

#FILES="/data/bills/mdenny_copy_early2015/bills/*anno"
#FILES="/data/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/*anno"
for (( c=0; c<100; c++ ))
do
    python pi.py
    find /data/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/ -type f -name '*.anno' | parallel --eta -j20 python shingling.py -doc {} -iter "$c"
done


python build_sketches.py
rm supershingles.txt
python supershingle.py $(find sketches -type f)

LC_ALL=C sort -k2 -n -t"," supershingles.txt

echo "[*] sorting"

LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted


echo "[*] finding candidates"
rm "shingles.congress.candidates"
python analyzer2.py  # make the candidates

echo "[*] finding jaccards"
rm shingles.congress.candidates.jacs


sort shingles.congress.candidates | uniq > t
mv t shingles.congress.candidates

cat shingles.congress.candidates | parallel python check_candidate.py {}


