FROM python:alpine3.10
RUN python -m pip install --upgrade pip
RUN MULTIDICT_NO_EXTENSIONS=1 pip install multidict
RUN pip install yarl charset-normalizer attrs async-timeout aiohttp
COPY server.py ./
EXPOSE 8008
CMD ["python", "./server.py" ]
