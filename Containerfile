FROM docker.io/library/python:3.12-bookworm

WORKDIR /app

RUN pip install kubernetes

ADD main.py /app/main.py

CMD ["/usr/local/bin/python3" ,"/app/main.py"]