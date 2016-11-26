echo "[*] shingling"
#for (( c=0; c<100; c++ ))
#do
rm shingles.congress
python pi.py
find demos_wilkerson -type f -name '*.anno' | parallel --eta -j20 python shingling.py -doc {} -iter NA
#done
LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted
