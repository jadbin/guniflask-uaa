FROM python:3.7

ADD ./ /opt/uaa
WORKDIR /opt/uaa

RUN chmod +x bin/manage \
  && pip install -r requirements/app.txt

CMD bin/manage start --daemon-off
