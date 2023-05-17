#!/bin/sh
# export NODE_OPTIONS=--max_old_space_size=4096
# yarn install
# clusterExternalDNS=`cat /etc/dcconfig/*.yaml | shyaml get-value clusterExternalDNS` 
# echo "clusterExternalDNS=${clusterExternalDNS}">.env.local
rm uiserver
yarn build
yarn start