import time
import schedule
from application.exporter import exporter
from worker import work


@schedule.repeat(schedule.every().day.at('19:28'))
def get_metrics_day():
    exporter(0, 'day')
    exporter(2, 'day')
    exporter(3, 'day')


@schedule.repeat(schedule.every().day.at('13:08'))
def get_metrics_day():
    work(0, 'day')


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
