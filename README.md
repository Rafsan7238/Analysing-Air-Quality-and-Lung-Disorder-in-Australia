    FOR COMP90024 ASSIGNMENT 2
    BY TEAM 45: 
        William Chen 1400081
        Petr Andreev 1375858
        Rafsan Al Mamun 1407776
        Ojaswi Dheer 1447227

# COMP90024_Assignment-2
This repo contains the assignment 2 files for COMP90024: Cluster and Cloud Programming at the University of Melbourne.

## Admins
    William Chen wilchen2@student.unimelb.edu.au
    Petr Andreev p.andreev@student.unimelb.edu.au
    Rafsan Al Mamun ralmamun@student.unimelb.edu.au
    Ojaswi Dheer ojaswi.dheer@student.unimelb.edu.au

## Setup
### Installation
 - As with the assignment class repository, you should install the below:
   - OpenStack clients 6.3.x ([Installation instructions](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)).
  > Note: Please ensure the following Openstack clients are installed: `python-cinderclient`, `python-keystoneclient`, `python-magnumclient`, `python-neutronclient`, `python-novaclient`, `python-octaviaclient`. See: [Install the OpenStack client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html).
   - JQ 1.6.x ([Installation instructions](https://jqlang.github.io/jq/download/)).
   - Kubectl 1.26.8 ([Installation instructions](https://kubernetes.io/docs/tasks/tools/)).
   - Helm 3.6.3 ([Installation instructions](https://helm.sh/docs/intro/install/)).
   - Connect to [Campus network](https://studentit.unimelb.edu.au/wifi-vpn#uniwireless) if on-campus or [UniMelb Student VPN](https://studentit.unimelb.edu.au/wifi-vpn#vpn) if off-campus
 - Get access to this project and create a key pair in MRC. Send the **public** key to an admin. Place the private key in you machines `~/.ssh` directory.
    - Tighten access to this key `chmod 600 ~/.ssh/{key name}.pem`.
 - Once your access key has been added to the project, you will be given a Kube config file. Add it to a folder called `.kube` in this project.
    - As with the ssh key, run `chmod 600 ~/.kube/config`.

### Connecting to the cluster
 - Ensure you are on the Unimelb campus network, either using the campus wifi or through the [student VPN](https://studentit.unimelb.edu.au/wifi-vpn#vpn)!
 - ssh into the cluster bastion node 
     `ssh -i ~/.ssh/{key name as made in installation}.pem -L 6443:192.168.10.153:6443 ubuntu@172.26.134.24`

 - Port-forward the cluster's Fission router to your localhost. Run the below in a separate terminal.
    `kubectl port-forward service/router -n fission 9090:80`

 - Optionally, forward the cluster's kibana port to your localhost. Run the below in yet another separate terminal. This will give you local access to the kibana dashboard.
    `kubectl port-forward service/kibana-kibana -n elastic 5601:5601`

### Seeing function logs
 - You can see the running logs of the repeating harvesters by using the lines 

    `fission function log -f --name addobservations`
    `fission function log -f --name mharvester`

## Usage
### Static data manipulation
The notebook for manipulating elastic search indexes and documents is `data/elstic_management_notebook.ipynb`. This notebook contains functioning requests that can be used to create all indexes (existing indexes will be ignored) and/or upload data to these indexes. 

Note that this notebook can only upload data to the static file indexes. Therefore it has intentional limitations:
 - It can only insert data if the index is empty.
    - The exception is the very large hourly air quality file which requires uploads in batches.
    - The only means to delete an index is to delete it through Kibana, this makes it more difficult to accidentally delete any indexes.
 - It can create the indexes for the two data sources with regular harvesting (see below), but it cannot add any data to these indexes.

This notebook also contains requests which will backfill data that is normally ingested automatically. This is intended only for when an index needs to be recreated for whatever reason. Running them will not do anything if the data is up to date.

### Automatic data manipulation
There are two regularly updating data sources. Mastodon, and BOM (Bureau of Meteorology). These data sources are regularly added to via fission functions triggered by timers. The Mastodon set is updated every 5 minutes, the BOM set is updated every 15 minutes.

### Analytics
There are two notebooks for requesting data from elastic search and displaying comprehensive statistical analytics. As the names suggest, "Air Quality vs Lung Disease Analysis.ipynb" provides the correlation analysis related to air quality, mainly PM2.5, and lung-related disorders in Victoria, while "Weather vs Sentiment Analysis.ipynb" contains the analysis related to the correlation between weather parameters and people's mood in Australia. Both the notebooks follow a storytelling format for easy comprehension of the analyses for the users. 

### Direct API Access
The APIs that are exposed, and used by the notebooks mentioned above, are:
 - POST `/elastic/{index}/documents` where 'index' is the name of the index in which to insert documents.
    - Valid index values can be found in `backend/constants.py`
    - This endpoint requires data to be present in the body in JSON format and the request must have request type `application/json`.
    - Is used in elastic_management_notebook.ipynb
 - POST `/indexes/create/all`
    - Creates any indexes which are missing. Ignores indexes which already exist. No body required.
    - Is used in elastic_management_notebook.ipynb
 - GET `/data/{resource_category}/{resource}`.
    - Valid resource categories are `air_quality`, or `sentiment_weather`.
    - Valid resources are in `backend/querying/query_path_constants.py`.
    - EG, to see the data for summary statistics of air quality, the http request would be GET `http://localhost:9090/data/air_quality/data_distribution`.


## Development
To upload any backend changes, run `sh publish_backend.sh` in the root directory of this project. This will:
 - Package everything in `backend/` into a zip file.
 - Wipe all fission packages, functions, and triggers.
 - Recreate all fission packages, functions, and triggers using the zipped archive.

To reset the python and nodejs environments, run `sh refresh_environments.sh` in the backend directory.

## Tests
To run tests execute `pytest tests/fission_tests.py` from project directory 
