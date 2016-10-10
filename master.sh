## Prelim stuff

rm demos/*anno
python makedemos.py

## Real stuff

# ./window.sh # make windows

#DOES NOT WORK W/O LC_ALL=C :( 
#http://man7.org/linux/man-pages/man1/sort.1.html
LC_ALL=C sort -k2 -n -t"," shingles.congress > shingles.congress.sorted

# confirm it works ... 
# cat shingles.congress.sorted | grep -n 3701186712771929879879506402213209889 | cut -f1 -d:

python analyzer2.py