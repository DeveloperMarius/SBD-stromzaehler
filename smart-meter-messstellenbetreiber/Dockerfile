FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY res res
COPY src src
COPY requirements.txt .

RUN apt-get update && apt-get install sqlite3

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "--app", "src/app.py", "run", "--host=0.0.0.0"]