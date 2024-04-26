# BY TEAM 45: 
#     William Chen 1400081
#     Petr Andreev 1375858
#     Rafsan Al Mamun 1407776
#     Xinran Li 1549584
#     Ojaswi Dheer 1447227

### ENV SETUP
fission env create --name python --image fission/python-env --builder fission/python-builder --verbosity=0;
fission env create --name nodejs --image fission/node-env --builder fission/node-builder --verbosity=0;

### HEALTHCHECK
fission function create --name health --env python --code backend/utils/health.py --verbosity=0;
# fission function test --name health | jq '.'

fission route create --url /health --function health --name health --createingress --verbosity=0;

### FISSION
backend/elastic/package.sh
fission package create --sourcearchive elastic.zip --env python --name elastic --buildcmd './build.sh' --verbosity=0;

### INDEX CREATION
fission fn create --name create-indexes --pkg elastic --env python --entrypoint "elastic.create_indexes" --verbosity=0;
fission route create --url /create-indexes --function create-indexes --name create-indexes --createingress --verbosity=0;

### HISTORIC TWEET INSERTION
fission fn create --name insert-hist-tweets --pkg elastic --env python --entrypoint "elastic.insert_hist_tweets" --verbosity=0;
fission route create --url /insert-hist-tweets --function insert-hist-tweets --name insert-hist-tweets --createingress --verbosity=0;
