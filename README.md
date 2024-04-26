# COMP90024_Assignment-2
This repo contains the assignment 2 files for COMP90024: Cluster and Cloud Programming at the University of Melbourne.

## Environment
Install stuff, set up clusters, install software.

1. Connect to unimelb VPN.
2. Start a docker runtime on your machine.
3. Run Docker Compose in root folder.
    - `docker-compose up`
    - This will compose a local docker container that install all dev dependencies.
4. Place a private ssh key as generated in MRC into a folder called `.ssh` in the root project.
    - Note that the .ssh folder is gitignore'd and this should always be the case forever and always.
    - Remember to restrict file access to this ssh key by running `chmod 600 ~/.ssh/{key name}.pem`. 
    - `chmod 600` prevents read and write access from any other users on your machine.
5. Using a shell attached to this docker container, connect to the bastion node.
    - `ssh -i ~/.ssh/{key name}.pem -L 6443:192.168.10.153:6443 ubuntu@172.26.134.24`
    - Remember that after any ssh connection or port forward request, you should keep that terminal open and open a new one for further interaction with the cloud system.
6. Obtain the Kube config from an Admin and add it to a folder called `.kube` in the root project.
    - As with the ssh key, run `chmod 600 ~/.kube/config`.
??? I couldn't actually get the docker to work, I'm just using wsl right now.

## Setting up
1. Set up fission by running fission_startup.sh
    - This will generate the packages used by fission
    - These packages will be used to create fission functions
    - These functions will get exposed in the endpoints described in the readme in `backend`

todo:
 - add content description to this readme.
 - add installation instructions???
 - add instructions on how to use the client.