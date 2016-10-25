foo=$1
one=$(echo $foo | cut -d "," -f 1)
two=$(echo $foo | cut -d "," -f 2)
sort -o $one $one # comm wants lexiographic sort not numeric sort la la la i hate computers
sort -o $two $two
a=$(comm -12 $one $two | wc -l)
echo $one,$two,$a>> pairs.txt