# Analysing the Relationship Between Air Quality and Lung Disorder in Australia

## Project Overview
This project demonstrates the use of cloud computing for data analysis, focusing on understanding critical aspects of life in Australia. Specifically, it explores the relationships between air quality and lung-related disorders, and the influence of weather patterns on mental health. Built on a robust cloud stack, this project leverages a scalable and event-driven architecture to ingest, process, and analyze large datasets related to health, weather, and public sentiment.

**[YouTube Video Overview](https://youtu.be/fhftcsxGKWA)**

## Admins
    William Chen wilchen2@student.unimelb.edu.au
    Petr Andreev p.andreev@student.unimelb.edu.au
    Rafsan Al Mamun ralmamun@student.unimelb.edu.au
    Ojaswi Dheer ojaswi.dheer@student.unimelb.edu.au

## Key Features
- **Cloud Infrastructure**: Hosted on the Melbourne Research Cloud, utilizing OpenStack and Kubernetes to manage efficient data processing and resource allocation.
- **Data Processing and Storage**: Serverless functions managed by Fission for event-based data processing, with ElasticSearch providing large-scale data storage and quick data retrieval.
- **Scenarios Analyzed**:
  - **Air Quality and Lung Disorders**: Analyzes correlations between PM2.5 levels and lung disease rates, offering insights for policymakers and public health.
  - **Weather and Mood**: Examines potential links between weather patterns and public mood by analyzing weather data alongside social media sentiment.
- **Interactive Analytics**: Jupyter Notebooks are used as the front-end interface, offering interactive data exploration, visualization, and in-depth analysis.

## Technology Stack
- **Kubernetes & Fission**: Orchestrates and deploys serverless functions, enabling an event-driven architecture.
- **ElasticSearch**: Indexes and stores large volumes of data for efficient querying and real-time analytics.
- **Jupyter Notebooks**: Allows for interactive data analysis and visualization, ideal for presenting insights and engaging stakeholders.

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
