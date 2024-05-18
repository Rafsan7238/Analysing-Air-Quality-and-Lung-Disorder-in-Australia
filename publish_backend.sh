

chmod +x backend/build.sh 
chmod +x backend/fission_wipe.sh 
chmod +x backend/fission_startup.sh
#!/bin/sh

# Recreate Fission Objects
backend/fission_wipe.sh
backend/fission_startup.sh

