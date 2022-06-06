#!/usr/bin/env bash
echo '==============================================='
echo 'Stop and remove old containers ...'
echo '==============================================='
echo ''
docker rm -f $(docker stop -t 1 $(docker ps -a -q --filter ancestor=python-http-server-alpine --format="{{.ID}}"))

echo '==============================================='
echo 'Rebuild container ...'
echo '==============================================='
echo ''
docker image build -t python-http-server-alpine .

echo '==============================================='
echo 'Starting new containers ...'
echo '==============================================='
echo ''
for i in {8000..8050}
do
    docker run -d -p $i:8008 -it python-http-server-alpine
done
