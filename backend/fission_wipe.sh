# BY TEAM 45: 
#     William Chen 1400081
#     Petr Andreev 1375858
#     Rafsan Al Mamun 1407776
#     Xinran Li 1549584
#     Ojaswi Dheer 1447227

# Wipe fission state
fission function delete --name health --ignorenotfound --verbosity=0 ;
fission httptrigger delete --name health --ignorenotfound --verbosity=0;

fission httptrigger delete --name create-indexes --ignorenotfound --verbosity=0;
fission function delete --name create-indexes --ignorenotfound --verbosity=0;

fission httptrigger delete --name insert-all --ignorenotfound  --verbosity=0;
fission function delete --name insert-all --ignorenotfound --verbosity=0;

fission function delete --name insert-indexes --ignorenotfound --verbosity=0;
fission httptrigger delete --name insert-indexes --ignorenotfound --verbosity=0;

fission package delete -f --name backend --ignorenotfound --verbosity=0;
fission package delete -f --name addobservations --ignorenotfound --verbosity=0;
fission package delete -f --name mharvester --ignorenotfound --verbosity=0;


fission function delete --name get-air-quality-hourly-avg --ignorenotfound --verbosity=0;
fission httptrigger delete --name get-air-quality-hourly-avg --ignorenotfound --verbosity=0;

fission function delete --name get-index --ignorenotfound --verbosity=0;
fission httptrigger delete --name get-index --ignorenotfound --verbosity=0;

fission function delete --name addobservations --ignorenotfound --verbosity=0;
fission function delete --name mharvester --ignorenotfound --verbosity=0;

fission timetrigger delete --name bom-harvester-repeater --ignorenotfound --verbosity=0;
fission timetrigger delete --name mastodon-harvester-repeater --ignorenotfound --verbosity=0;

fission package delete --name addobservations -f --ignorenotfound --verbosity=0;
fission package delete --name mharvester -f --ignorenotfound --verbosity=0;

