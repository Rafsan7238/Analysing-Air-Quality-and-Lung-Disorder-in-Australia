# BY TEAM 45: 
#     William Chen 1400081
#     Petr Andreev 1375858
#     Rafsan Al Mamun 1407776
#     Xinran Li 1549584
#     Ojaswi Dheer 1447227

# Wipe fission state
### Health
fission function delete --name health --ignorenotfound --verbosity=0;
fission httptrigger delete --name health --ignorenotfound --verbosity=0;

### Observation
fission timetrigger delete --name bom-harvester-repeater --ignorenotfound --verbosity=0;
fission function delete --name addobservations --ignorenotfound --verbosity=0;
fission package delete -f --name addobservations --ignorenotfound --verbosity=0;

### Mastodon
fission timetrigger delete --name mastodon-harvester-repeater --ignorenotfound --verbosity=0;
fission function delete --name mharvester --ignorenotfound --verbosity=0;
fission package delete --name mharvester -f --ignorenotfound --verbosity=0;

### Index Management
fission httptrigger delete --name create-indexes --ignorenotfound --verbosity=0;
fission function delete --name create-indexes --ignorenotfound --verbosity=0;

fission function delete --name insert-documents --ignorenotfound --verbosity=0;
fission httptrigger delete --name insert-documents --ignorenotfound --verbosity=0;

### Extraction Endpoints
fission httptrigger delete --name make-sql-query  --ignorenotfound --verbosity=0;
fission function delete --name make-sql-query --ignorenotfound --verbosity=0;

fission httptrigger delete --name get-air-quality-data  --ignorenotfound --verbosity=0;
fission function delete --name get-air-quality-data --ignorenotfound --verbosity=0;

fission function delete --name get-all-from-index --ignorenotfound --verbosity=0;
fission httptrigger delete --name get-all-from-index --ignorenotfound --verbosity=0;

fission function delete --name get-sentiment-weather-query --ignorenotfound --verbosity=0;
fission httptrigger delete --name get-sentiment-weather-query --ignorenotfound --verbosity=0;

### Package Delete
fission package delete -f --name backend --ignorenotfound --verbosity=0;

