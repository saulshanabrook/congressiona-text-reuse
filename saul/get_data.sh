# This stuff is from Abe
rsync -avz govtrack.us::govtrackdata/congress/113/bills govtrackdata

# find all votes files and bills files
find . -name document.xml -type f > all.txt
find govtrakdata/votes/ -name data.xml > votesfiles.txt

# break bills into sections based on the govtrack assigned section GUID
mkdir sections
python xmlreader.py

# run StanfordCORENLP
python annotate.py

python ulman.py

# This stuff is from Saul
rsync -avzR --delete --delete-excluded --exclude "*/data.xml"  govtrack.us::govtrackdata/congress/113/votes/ govtrackdata/

rsync -avzR --delete --delete-excluded --exclude "*.yaml" --exclude "*/committee*"   govtrack.us::govtrackdata/congress-legislators/ govtrackdata/