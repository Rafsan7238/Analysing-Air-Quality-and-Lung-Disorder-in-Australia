fission env create --name python --image fission/python-env --builder fission/python-builder
fission env create --name nodejs --image fission/node-env --builder fission/node-builder

fission function create --name bomharvester --env python --code backend/utils/bom_harvester.py
fission function test --name bomharvester | jq '.'

fission route create --url /bomharvester --function bomharvester --name bomharvester --createingress
