FROM python:alpine3.10
COPY server.py ./
EXPOSE 8008
CMD ["python", "./server.py" ]