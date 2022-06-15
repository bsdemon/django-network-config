# Build project

- Python 3.10 is required
- Redis > 5.0.0

## Clone project

```git clone https://github.com/bsdemon/django-network-config.git```

cd <_repository_folder_>

## Set up virtual environment

```pip install virtualenv```

```virtualenv -p /usr/bin/python3.10 venv```

## Activate virtual environment

```source venv/bin/activate```

## Install requirements

```pip install -r requirements.txt```

## .env file

- Add `.env` file in `settings.py` directory.

```# Django settings
SECRET_KEY='django-insecure-jlh9$s&5(695xdw=yawx*#f4a1apnu4+o$@5&b1^%*f_&9mcd$'

# Redis settings
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_DB=1
REDIS_CHANNEL='django_network_config'
REDIS_Q_CHANNEL='task_Q'
```

## run Django server and migrations

```cd django_network_config```

```python manage.py migrate```

```python manage.py createsuperuser```

```python manage.py runserver```

## in separate terminal with activated virtualenv run

```python ./manage.py dispatch_config```

## Build and start 20 docker dummy devices

```./start_dumy_devices.sh```

## Make 20 post request with Curl with payload

```./test_all.sh```

## API endpoints

```http://localhost:8000/api/get_all_running_tasks``` - Get all tasks

```http://localhost:8000/api/get_task_status/<_task.uuid_>``` - Get status for task with uuid

```http://localhost:8000/api/create_task``` - Create task with payload


<!-- ## Start redis container

docker run --name django-net-conf-redis -d redis

## Enter to redis-cli to monitor

docker exec -it django-net-conf-redis redis-cli -->