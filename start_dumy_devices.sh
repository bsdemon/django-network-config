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
echo 'Running docker network ...'
echo '==============================================='
echo ''
docker network create --subnet=10.10.10.0/24 --ip-range=10.10.10.0/24 --gateway=10.10.10.1 django_test_network

echo '==============================================='
echo 'Starting new containers ...'
echo '==============================================='
echo ''
for IP in 10.10.10.{2..100}
do
    docker run --network=django_test_network -tdi --ip $IP python-http-server-alpine
done
