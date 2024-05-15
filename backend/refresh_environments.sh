# These are fundamental, we should try to force their recreation but also warn if they could not be found.
fission env delete -f --name python --verbosity=0;
fission env delete -f --name nodejs --verbosity=0;

fission env create --name python --builder fission/python-builder-3.9 --image fission/python-env-3.9 --verbosity=0;
fission env create --name nodejs --image fission/node-env --builder fission/node-builder --verbosity=0;