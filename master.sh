## Prelim stuff

python makedemos.py

## Real stuff

#THIS DOES NOT WORK W/O LC_ALL=C 
#http://man7.org/linux/man-pages/man1/sort.1.html

# RUN STUFF MANUALLY IN THE SHINGLING FILE HERE FOR NOW BAD TODO

LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted

rm "shingles.congress.candidates"
python analyzer2.py  # make the candidates

rm "shingles.congress.candidates.jacs"
FILENAME="shingles.congress.candidates"
cat $FILENAME | while read LINE
do
python check_candidate.py "$LINE"
done