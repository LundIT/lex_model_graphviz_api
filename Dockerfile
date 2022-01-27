FROM python:3.9

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y graphviz && pip install -r requirements.txt

CMD python3 json_to_graphviz_svg.py