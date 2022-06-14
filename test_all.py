#!/usr/bin/env bash

echo '==============================================='
echo 'Send curl requests ...'
echo '==============================================='
echo ''
# declare -a ip_range=("10.10.10.2" "10.10.10.3" "10.10.10.2" "10.10.10.3" "10.10.10.4" "10.10.10.4"\
# "10.10.10.5" "10.10.10.6" "10.10.10.7" "10.10.10.8" "10.10.10.9" "10.10.10.10" "10.10.10.11" "10.10.10.12")
# for IP in "${ip_range[@]}"

for IP in 10.10.10.{2..100}
do
    curl -X POST -H "Content-Type: application/json" -d \
    '{"hostname": "sof-lab-'$IP'", "port": 8008, "ip": "'$IP'", "configuration": "configure terminal\ninterface xg0/0/1\nvlan 10 type tagged\nvlan 11 type tagged\nmac-address-learning disable\nmac-address static de:ad:00:be:ef:00:01\nsave\n" }' \
  http://localhost:8000/api/create_task

  echo '\n'
done


# {
#     "hostname": "sof-lab-1",
#     "port": 8008,
#     "ip": "10.10.10.4",
#     "configuration": "configure terminal\ninterface xg0/0/1\nvlan 10 type tagged\nvlan 11 type tagged\nmac-address-learning disable\nmac-address static de:ad:00:be:ef:00:01\nsave\n" 
# }

# {
#     "hostname": "sof-lab-2",
#     "port": 8008,
#     "ip": "10.10.10.2",
#     "configuration": "configure terminal\ninterface xg0/0/1\nvlan 10 type tagged\nvlan 11 type tagged\nmac-address-learning disable\nmac-address static de:ad:00:be:ef:00:01\nsave\n" 
# }


#     curl -X POST -H "Content-Type: application/json" -d \
#     '{"hostname": "sof-lab-2", "port": 8008, "ip": "10.10.10.2", "configuration": "configure terminal\ninterface xg0/0/1\nvlan 10 type tagged\nvlan 11 type tagged\nmac-address-learning disable\nmac-address static de:ad:00:be:ef:00:01\nsave\n" }' \
#   http://localhost:8000/api/create_task




