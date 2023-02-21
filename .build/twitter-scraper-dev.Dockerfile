FROM python:3.9
WORKDIR /app

ENV NODE_ENV=dev

COPY services/twitter-scraper/ ./

RUN pip3 install requests schedule

CMD ["python3", "main.py"]