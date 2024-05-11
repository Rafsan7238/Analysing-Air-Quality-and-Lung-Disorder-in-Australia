#!/bin/sh

rm -f *.zip

# Package backend
(
    cd backend
    zip -r ../backend.zip .
)

zip -r backend.zip database data -x data/2022_All_sites_air_quality_hourly_avg.xlsx
# kubectl apply -f data/data-map.yaml

# Recreate Fission Objects
backend/fission_wipe.sh
backend/fission_startup.sh

