import time
import schedule
from application.exporter import exporter
from worker import work


@schedule.repeat(schedule.every().day.at('16:03'))
def get_metrics_day():
    exporter('vkus', 'day')


@schedule.repeat(schedule.every().day.at('16:12'))
def get_metrics_day():
    work('vkus', 'day')


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
