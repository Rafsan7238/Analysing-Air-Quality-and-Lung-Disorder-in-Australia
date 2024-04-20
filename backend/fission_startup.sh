fission env create --name python --image fission/python-env --builder fission/python-builder
fission env create --name nodejs --image fission/node-env --builder fission/node-builder

fission function create --name health --env python --code backend/utils/health.py
fission function test --name health | jq '.'

fission route create --url /health --function health --name health --createingress
