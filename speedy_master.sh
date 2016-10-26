rm shingles.congress.candidates
for (( c=0; c<100; c++ ))
do
    ./speedy.sh
done

awk -F, -f finalcount.awk shingles.congress.candidates