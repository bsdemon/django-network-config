# Build project

- Python 3.10 is reuired
## Clone project

- git clone <_repository_>

- cd <_repository_folder_>

## Set up virtual environment

- pip install virtualenv

- virtualenv -p /usr/bin/python3.10 DjangoNetConf_venv

- source DjangoNetConf_venv/bin/activate

- pip install -r requirements.txt

## Build docker image

- docker image build -t python-http-server-alpine .

- ./start_dumy_devices.sh

## Notes for dev env
- Set env var PYTHONDEVMODE=1 (it includes PYTHONASYNCIODEBUG=1)
