SSH login `ssh -i .keys/comp90024 -L 6443:192.168.10.153:6443 ubuntu@172.26.134.24`

RUN `fission_startup.sh` to create environments and functions 
once function is created run in a new shell `fission function log -f --name <func_name>` to enable logging. 

## Endpoints
The fission url root is `http://127.0.0.1:9090`.
 - `/health`: returns the current state of the ElasticSearch cluster.
 - `/create-indexes`: creates all indexes if they do not exist.


To access fission `kubectl port-forward service/router -n fission 9090:80`
To access elastic search `kubectl port-forward service/elasticsearch-master -n elastic 9200:9200`

To access kibanan `kubectl port-forward service/kibana-kibana -n elastic 5601:5601`


The kibana url is `http://127.0.0.1:5601`

