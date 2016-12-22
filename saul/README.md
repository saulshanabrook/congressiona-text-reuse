# Ideal Point Estimation

## Requirements
Docker, Docker Compose, and rsync.

## Setup

Download all vote data and legislator data:

```bash
rsync -avzR --delete --delete-excluded --exclude "*/data.xml"  govtrack.us::govtrackdata/congress/113/votes/ govtrackdata/
rsync -avzR --delete --delete-excluded --exclude "*/*.html" --exclude "*/*.xml" govtrack.us::govtrackdata/congress/113/bills/ govtrackdata/

rsync -avzR --delete --delete-excluded --exclude "*.yaml" --exclude "*/committee*"   govtrack.us::govtrackdata/congress-legislators/ govtrackdata/
```

Start the app

```bash
docker-compose up --build
```


## Usage

Check out `./notebooks/ideal point.ipynb` for example usage


```bash
open 'http://localhost:8888/notebooks/ideal%20point.ipynb'
```


## Directory Structure

We don't want to mount `govtrackdata` as a volume in the Docker container, because this causes much slower file IO 
when using Docker for Mac. So instead, we include this data
in our container, and put all editable files in subdirectories, so we can mount them in volumes in the container.
