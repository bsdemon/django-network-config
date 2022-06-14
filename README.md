# Build project

- Python 3.10 is required
- Redis > 5.0.0

## Clone project

git clone <_repository_>

cd <_repository_folder_>

## Set up virtual environment

pip install virtualenv

virtualenv -p /usr/bin/python3.10 venv

source venv/bin/activate

pip install -r requirements.txt

## Build and start docker dummy devices

- ./start_dumy_devices.sh

<!-- ## Start redis container

docker run --name django-net-conf-redis -d redis

## Enter to redis-cli to monitor

docker exec -it django-net-conf-redis redis-cli -->