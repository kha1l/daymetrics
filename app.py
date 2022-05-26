import time
import schedule
from application.exporter import exporter
from application.writer import writer


@schedule.repeat(schedule.every().day.at('17:09'))
def get_metrics_day():
    exporter(0, 'day')
    exporter(2, 'day')
    exporter(3, 'day')


@schedule.repeat(schedule.every().day.at('16:40'))
def write_metrics_day():
    writer(0, 'day')
    writer(2, 'day')
    writer(3, 'day')


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
