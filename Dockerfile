FROM python:3.9

WORKDIR /app
COPY . .

RUN apt-get update \
    && apt-get install -y graphviz \
    && pip install -r requirements.txt \
    && apt-get install -y git

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 wrapper:app
