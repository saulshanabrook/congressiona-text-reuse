 #!/bin/bash 
COUNTER=108
while [  $COUNTER -lt 114 ]; do
    echo The counter is $COUNTER
    find govtrackdata/$COUNTER/bills -name document.xml > $COUNTER.txt
    python xmlreader.py $COUNTER
    let COUNTER=COUNTER+1
done
python annotate.py
python ulman.py
