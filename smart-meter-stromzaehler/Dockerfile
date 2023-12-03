FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY res res
COPY src src
COPY requirements.txt .

RUN apt-get update && apt-get -y install sqlite3 cron

RUN pip3 install -r requirements.txt

RUN cd res && chmod +x ./setup.sh && ./setup.sh && cd ..

RUN touch /var/log/cron.log
RUN (crontab -l ; echo "* * * * * /usr/local/bin/python3 /python-docker/src/app.py >>/var/log/cron.log") | crontab

CMD cron && tail -f /var/log/cron.log
