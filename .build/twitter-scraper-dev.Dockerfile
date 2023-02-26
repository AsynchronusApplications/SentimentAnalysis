FROM python:3.9
WORKDIR /app

ENV NODE_ENV=dev

COPY services/twitter-scraper/twitter_listener_proto.py ./

RUN pip3 install requests

CMD ["python3", "main.py"]