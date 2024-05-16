# Recreate Fission Objects

### PACKAGE
(   cd backend/;   zip -r backend.zip .;   mv backend.zip ../; )
fission package create --sourcearchive backend.zip --env python --name backend --buildcmd './build.sh' --verbosity=0;

### HEALTHCHECK
fission function create --name health --pkg backend --env python --entrypoint utils.health.main --verbosity=0;

fission route create --url /health --function health --name health --createingress --verbosity=0;

### INDEX CREATION
fission fn create --name create-indexes --pkg backend --env python --entrypoint "backend.create_indexes_endpoint" --fntimeout 360 --verbosity=0;
fission route create --method POST --url "/indexes/create/all" --function create-indexes --name create-indexes --createingress --verbosity=0;

### BOM HARVESTER PACKAGE
(   cd backend/harvesters/BOM/;   zip -r addobservations.zip .;   mv addobservations.zip ../; )
fission package create --sourcearchive backend/harvesters/addobservations.zip  --env python  --name addobservations  --buildcmd './build.sh' --verbosity=0;
fission fn create --name addobservations  --pkg addobservations  --env python  --entrypoint "addobservations.main" --fntimeout 360 --verbosity=0; 
fission timer create --name bom-harvester-repeater --function addobservations --cron "@every 15m" --verbosity=0;

### MASTODON HARVESTER
(   cd backend/harvesters/Mastodon/;   zip -r mharvester.zip .;   mv mharvester.zip ../; )
fission package create --sourcearchive backend/harvesters/mharvester.zip  --env python  --name mharvester  --buildcmd './build.sh' --verbosity=0;
fission fn create --name mharvester  --pkg mharvester  --env python  --entrypoint "mharvester.main" --fntimeout 240 --verbosity=0;
fission timer create --name mastodon-harvester-repeater --function mharvester --cron "@every 5m" --verbosity=0;

# ### GET ASTMA BY REGION 
fission fn create --name get-air-quality-hourly-avg --pkg backend --env python --entrypoint "backend.get_air_quality_hourly_avg" --verbosity=0;
fission route create --url "/air-quality-hourly-avg" --function get-air-quality-hourly-avg --name get-air-quality-hourly-avg --createingress --verbosity=0;

fission fn create --name get-index --pkg backend --env python --entrypoint "backend.get_index" --verbosity=0;

(
  fission route create --name get-index --function get-index \
    --method GET \
    --url '/datasets/{index}'
)

fission fn create --name insert-indexes --pkg backend --env python --entrypoint "backend.insert_indexes" --fntimeout 120 --verbosity=0;

(
  fission route create --name insert-indexes --function insert-indexes \
    --method POST \
    --url '/elastic/{index}/documents' --verbosity=0;
)

fission fn create --name make-sql-query --pkg backend --env python --entrypoint "backend.make_query_endpoint" --verbosity=0;
fission route create --method POST --url "/sql/query" --function make-sql-query --name make-sql-query --createingress --verbosity=0;
