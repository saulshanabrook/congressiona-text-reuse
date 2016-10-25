a=$(comm -12 $1 $2 | wc -l)
echo $1,$2,$a >> pairs.txt