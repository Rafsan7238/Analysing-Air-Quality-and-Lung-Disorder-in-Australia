# NOTE this aint gonna run just by itself
fission env create --name python --image fission/python-env --builder fission/python-builder
fission env create --name nodejs --image fission/node-env --builder fission/node-builder

fission function create --name bomharvester --env python --code backend/harvesters/BOM/bom_harvester.py
fission function test --name bomharvester | jq '.'

#fission route create --url /bomharvester --function bomharvester --name bomharvester --createingress
(   cd backend/harvesters/BOM/;   zip -r addobservations.zip .;   mv addobservations.zip ../; )

chmod +x build.sh

# or create 
fission package update --sourcearchive backend/harvesters/addobservations.zip  --env python  --name addobservations  --buildcmd './build.sh'

fission fn update --name addobservations  --pkg addobservations  --env python  --entrypoint "addobservations.main" 


