FROM python:3.6

ADD ./ /opt/uaa
WORKDIR /opt/uaa

RUN chmod +x bin/manage \
  && pip install -r requirements/app.txt

CMD bin/manage start --daemon-off
