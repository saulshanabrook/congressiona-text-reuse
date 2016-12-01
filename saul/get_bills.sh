 #!/bin/bash 
COUNTER=101
while [  $COUNTER -lt 114 ]; do
    echo The counter is $COUNTER
    mkdir govtrackdata/$COUNTER
    mkdir govtrackdata/$COUNTER/sections
    rsync -avz govtrack.us::govtrackdata/congress/$COUNTER/bills govtrackdata/$COUNTER/
    let COUNTER=COUNTER+1
done