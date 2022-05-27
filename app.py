import time
import schedule
from application.exporter import exporter
from worker import work


@schedule.repeat(schedule.every().day.at('21:51'))
def get_metrics_day():
    exporter(0, 'day')
    exporter(2, 'day')
    exporter(3, 'day')


@schedule.repeat(schedule.every().day.at('22:06'))
def get_metrics_day():
    work(0, 'day')
    work(2, 'day')
    work(3, 'day')


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
