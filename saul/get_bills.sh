 #!/bin/bash 
COUNTER=101
while [  $COUNTER -lt 114 ]; do
    echo The counter is $COUNTER
    rsync -avz govtrack.us::govtrackdata/congress/$COUNTER/bills govtrackdata
    let COUNTER=COUNTER+1
done