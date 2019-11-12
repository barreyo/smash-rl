
FROM python:3.7-buster

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]

