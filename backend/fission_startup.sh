# Recreate Fission Objects

### PACKAGE
rm -f *.zip

(   cd backend/;   zip -r backend.zip .;   mv backend.zip ../; )
fission package create --sourcearchive backend.zip --env python --name backend --buildcmd './build.sh' --verbosity=0;

### HEALTHCHECK
fission function create --name health --pkg backend --env python --entrypoint utils.health.main --verbosity=0;

fission route create --url /health --function health --name health --createingress --verbosity=0;

### BOM HARVESTER PACKAGE
(   cd backend/harvesters/BOM/;   zip -r addobservations.zip .;   mv addobservations.zip ../; )
fission package create --sourcearchive backend/harvesters/addobservations.zip  --env python  --name addobservations  --buildcmd './build.sh' --verbosity=0;
fission fn create --name addobservations  --pkg addobservations  --env python  --entrypoint "addobservations.main" --fntimeout 360 --verbosity=0; 
fission timer create --name bom-harvester-repeater --function addobservations --cron "@every 15m" --verbosity=0;

### MASTODON HARVESTER
(   cd backend/harvesters/Mastodon/;   zip -r mharvester.zip .;   mv mharvester.zip ../; )
fission package create --sourcearchive backend/harvesters/mharvester.zip  --env python  --name mharvester  --buildcmd './build.sh' --verbosity=0;
fission fn create --name mharvester  --pkg mharvester  --env python  --entrypoint "mharvester.main" --fntimeout 360 --verbosity=0;
fission timer create --name mastodon-harvester-repeater --function mharvester --cron "@every 5m" --verbosity=0;

### Index Management
fission fn create --name create-indexes --pkg backend --env python --entrypoint "backend.create_indexes_endpoint" --fntimeout 360 --verbosity=0;
fission route create --method POST --url "/indexes/create/all" --function create-indexes --name create-indexes --createingress --verbosity=0;

fission fn create --name insert-documents --pkg backend --env python --entrypoint "backend.insert_documents" --fntimeout 360 --verbosity=0;
(
  fission route create --name insert-documents --function insert-documents \
    --method POST \
    --url '/elastic/{index}/documents' --verbosity=0;
)

### Extraction Endpoints

fission fn create --name make-sql-query --pkg backend --env python --entrypoint "backend.make_query_endpoint" --verbosity=0;
fission route create --method POST --url "/sql/query" --function make-sql-query --name make-sql-query --createingress --verbosity=0;

fission fn create --name get-air-quality-data --pkg backend --env python --entrypoint "backend.air_quality_endpoint" --verbosity=0;
(
  fission route create --name get-air-quality-data --function get-air-quality-data \
    --method GET \
    --url '/data/air_quality/{resource}' --verbosity=0;
)

fission fn create --name get-all-from-index --pkg backend --env python --entrypoint "backend.select_all_from_index" --verbosity=0;
(
  fission route create --name get-all-from-index --function get-all-from-index \
    --method GET \
    --url '/data/{index}/all' --verbosity=0;
)

fission fn create --name get-sentiment-weather-query --pkg backend --env python --entrypoint "backend.sentiment_weather_queries_endpoint" --verbosity=0;
(
  fission route create --name get-sentiment-weather-query --function get-sentiment-weather-query \
    --method GET \
    --url '/data/sentiment_weather/{resource}' --verbosity=0;
)