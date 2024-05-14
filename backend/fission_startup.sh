# Recreate Fission Objects

### ENV SETUP
fission env create --name python --builder fission/python-builder-3.9 --image fission/python-env-3.9 --verbosity=0;
fission env create --name nodejs --image fission/node-env --builder fission/node-builder --verbosity=0;

### PACKAGE
fission package create --sourcearchive backend.zip --env python --name backend --buildcmd './build.sh' --verbosity=0;

### HEALTHCHECK
fission function create --name health --pkg backend --env python --entrypoint utils.health.main --verbosity=0;

fission route create --url /health --function health --name health --createingress --verbosity=0;

### INDEX CREATION
fission fn create --name create-indexes --pkg backend --env python --entrypoint "backend.create_indexes_endpoint" --fntimeout 360 --verbosity=0;
fission route create --method POST --url "/indexes/create/all" --function create-indexes --name create-indexes --createingress --verbosity=0;

### BOM HARVESTER PACKAGE
(   cd backend/harvesters/BOM/;   zip -r addobservations.zip .;   mv addobservations.zip ../; )
fission package create --sourcearchive backend/harvesters/addobservations.zip  --env python  --name addobservations  --buildcmd './build.sh'
fission fn create --name addobservations  --pkg addobservations  --env python  --entrypoint "addobservations.main" 
fission timer create --name bom-harvester-repeater --function addobservations --cron "@every 15m"

### MASTODON HARVESTER
(   cd backend/harvesters/Mastodon/;   zip -r mharvester.zip .;   mv mharvester.zip ../; )
fission package create --sourcearchive backend/harvesters/mharvester.zip  --env python  --name mharvester  --buildcmd './build.sh'
fission fn create --name mharvester  --pkg mharvester  --env python  --entrypoint "mharvester.main" 
fission timer create --name mastodon-harvester-repeater --function mharvester --cron "@every 5m"

fission fn create --name insert-indexes --pkg backend --env python --entrypoint "backend.insert_indexes" --verbosity=0  --fntimeout 120;

(
  fission route create --name insert-indexes --function insert-indexes \
    --method POST \
    --url '/elastic/{index}/documents'
)