FROM python:3.9

WORKDIR /app

COPY ../services/twitter-scraper/twitter_listener_proto.py ./

RUN pip install requests

CMD ["python3", "./twitter_listener_proto.py"]