## Prelim stuff
# python makedemos.py

## Real stuff

#THIS DOES NOT WORK W/O LC_ALL=C 
#http://man7.org/linux/man-pages/man1/sort.1.html

echo "fn,digit,window_no,window_size,iter" > "shingles.congress"

echo "[*] shingling"

FILES="demos_congress/*anno"
for (( c=1; c<=1000; c++ ))
do
    python pi.py
    for f in $FILES
    do
        python shingling.py -doc "$f" -iter "$c"
    done
done

echo "[*] sorting"

LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted


echo "[*] finding candidates"
rm "shingles.congress.candidates"
python analyzer2.py  # make the candidates

echo "[*] finding jaccards"
rm "shingles.congress.candidates.jacs"
FILENAME="shingles.congress.candidates"
cat $FILENAME | while read LINE
do
   python check_candidate.py "$LINE"
done