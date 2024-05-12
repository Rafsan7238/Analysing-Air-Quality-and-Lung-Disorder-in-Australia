# BY TEAM 45: 
#     William Chen 1400081
#     Petr Andreev 1375858
#     Rafsan Al Mamun 1407776
#     Xinran Li 1549584
#     Ojaswi Dheer 1447227

# Wipe fission state
fission function delete --name health --ignorenotfound --verbosity=0;
fission httptrigger delete --name health --ignorenotfound --verbosity=0;

fission httptrigger delete --name create-indexes --ignorenotfound --verbosity=0;
fission function delete --name create-indexes --ignorenotfound --verbosity=0;

fission httptrigger delete --name insert-hist-tweets --ignorenotfound --verbosity=0;
fission function delete --name insert-hist-tweets --ignorenotfound --verbosity=0;

fission httptrigger delete --name insert-region-asthma --ignorenotfound  --verbosity=0;
fission function delete --name insert-region-asthma --ignorenotfound --verbosity=0;

fission package delete --name backend -f --ignorenotfound --verbosity=0; # force this as we have a tendency to create stuff from backend without including it here.

fission function delete --name addobservations --ignorenotfound --verbosity=0;
fission function delete --name mharvester --ignorenotfound --verbosity=0;

fission package delete --name addobservations -f --ignorenotfound --verbosity=0;
fission package delete --name mharvester -f --ignorenotfound --verbosity=0;

fission function delete --name insert-indexes --ignorenotfound --verbosity=0;
fission httptrigger delete --name insert-indexes --ignorenotfound --verbosity=0;

# These are fundamental, we should try to force their recreation but also warn if they could not be found.
fission env delete -f --name python --verbosity=0;
fission env delete -f --name nodejs --verbosity=0;