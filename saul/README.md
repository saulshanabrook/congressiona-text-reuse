# Ideal Point Estimation

## Requirements
Docker, Docker Compose, and rsync.

## Setup

Download all vote data and legislator data:

```bash
rsync -avzR --delete --delete-excluded --exclude "*/data.xml"  govtrack.us::govtrackdata/congress/113/votes/ govtrackdata/

rsync -avzR --delete --delete-excluded --exclude "*.yaml" --exclude "*/committee*"   govtrack.us::govtrackdata/congress-legislators/ govtrackdata/
```

Start the app

```bash
docker-compose up --build
```


## Usage

Check out `ideal point.ipynb` for example usage


```bash
open 'http://localhost:8888/notebooks/ideal%20point.ipynb'
```
