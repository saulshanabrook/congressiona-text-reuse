# This stuff is from Abe
rsync -avz govtrack.us::govtrackdata/congress/113/bills govtrackdata
rsync -avz govtrack.us::govtrackdata/congress/113/votes govtrackdata

# find all votes files
find . -name document.xml -type f > all.txtfind govtrakdata/votes -name data.xml > votesfiles.txt



# This stuff is from Saul
rsync -avzR --delete --delete-excluded --exclude "*/data.xml"  govtrack.us::govtrackdata/congress/113/votes/ govtrackdata/

rsync -avzR --delete --delete-excluded --exclude "*.yaml" --exclude "*/committee*"   govtrack.us::govtrackdata/congress-legislators/ govtrackdata/