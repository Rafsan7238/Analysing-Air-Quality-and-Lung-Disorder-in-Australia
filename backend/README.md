RUN `fission_startup.sh` to create environments and functions 
once function is created run in a new shell `fission function log -f --name <func_name>` to enable logging. 
To access elastic search `kubectl port-forward service/elasticsearch-master -n elastic 9200:9200`

