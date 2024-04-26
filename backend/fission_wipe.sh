# BY TEAM 45: 
#     William Chen 1400081
#     Petr Andreev 1375858
#     Rafsan Al Mamun 1407776
#     Xinran Li 1549584
#     Ojaswi Dheer 1447227
fission function delete --name health --verbosity=0;
fission httptrigger delete --name health --verbosity=0;

fission httptrigger delete --name create-indexes --verbosity=0;
fission function delete --name create-indexes --verbosity=0;

fission httptrigger delete --name insert-hist-tweets --verbosity=0;
fission function delete --name insert-hist-tweets --verbosity=0;

fission package delete --name elastic --verbosity=0;