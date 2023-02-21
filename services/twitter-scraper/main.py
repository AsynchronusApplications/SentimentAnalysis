import time  # Thread: Sleep
import datetime
import schedule  # Scheduler
import requests

def task_1(text:str):
    url = 'https://16b336b235e7f458c2cff4a428ef7780.m.pipedream.net'
    data = {
        "message": text
    }

    response = requests.post(url, json=data)
    print("response= ", response.json())

def task_2(text:str):
    print(text)


schedule.every().minute.at(":00").do(task_2, "Application#001: Hello World")

dt = datetime.datetime.now()
task_1(f"Twitter-Scraper started at {dt.strftime('%Y-%m-%d %H:%M:%S')}")

while True:
    schedule.run_pending()
    time.sleep(1)