# BY TEAM 45: 
#     William Chen 1400081
#     Petr Andreev 1375858
#     Rafsan Al Mamun 1407776
#     Xinran Li 1549584
#     Ojaswi Dheer 1447227

# Recreate Fission Objects

### ENV SETUP
fission env create --name python --image fission/python-env --builder fission/python-builder --verbosity=0;
fission env create --name nodejs --image fission/node-env --builder fission/node-builder --verbosity=0;

### PACKAGE
fission package create --sourcearchive backend.zip --env python --name backend --buildcmd './build.sh' --verbosity=0;

### HEALTHCHECK
fission function create --name health --pkg backend --env python --entrypoint utils.health.main --verbosity=0;
# fission function test --name health

fission route create --url /health --function health --name health --createingress --verbosity=0;
# curl "http://127.0.0.1:9090/health" 

### INDEX CREATION
fission fn create --name create-indexes --pkg backend --env python --entrypoint "backend.create_indexes_endpoint" --verbosity=0;
fission route create --url "/create/indexes" --function create-indexes --name create-indexes --createingress --verbosity=0;

# ### HISTORIC TWEET INSERTION
fission fn create --name insert-hist-tweets --pkg backend --env python --entrypoint "backend.insert_hist_tweets_endpoint" --verbosity=0;
fission route create --url "/insert/hist-tweets" --function insert-hist-tweets --name insert-hist-tweets --createingress --verbosity=0;


# ### ASTHMA BY REGION INSERTION
fission fn create --name insert-region-asthma --pkg backend --env python --entrypoint "backend.insert_region_asthma_endpoint" --verbosity=0;
fission route create --url "/insert/region-asthma" --function insert-region-asthma --name insert-region-asthma --createingress --verbosity=0;

### BOM HARVESTER PACKAGE
(   cd backend/harvesters/BOM/;   zip -r addobservations.zip .;   mv addobservations.zip ../; )
# chmod +x build.sh
# Update package (or create) 
fission package create --sourcearchive backend/harvesters/addobservations.zip  --env python  --name addobservations  --buildcmd './build.sh'
fission fn create --name addobservations  --pkg addobservations  --env python  --entrypoint "addobservations.main" 


### MASTODON HARVESTER
(   cd backend/harvesters/Mastodon/;   zip -r mharvester.zip .;   mv mharvester.zip ../; )
# Update package (or create) 
fission package create --sourcearchive backend/harvesters/mharvester.zip  --env python  --name mharvester  --buildcmd './build.sh'
fission fn create --name mharvester  --pkg mharvester  --env python  --entrypoint "mharvester.main" 
