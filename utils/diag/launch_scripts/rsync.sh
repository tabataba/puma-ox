#!/bin/bash

while [ 1 ]
do
    rsync --progress -avP ftabatabavakili@arcus-b.arc.ox.ac.uk:/data/pam/ftabatabavakili/pumagt_arcb_parameters .
    if [ "$?" = "0" ] ; then
        echo "rsync completed normally"
        exit
    else
        echo "rsync failure. Retrying in a minute..."
        sleep 10
    fi
done