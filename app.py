import time
import schedule
from application.exporter import exporter
from worker import work
from datetime import date, timedelta


# Экспорт Вересов
@schedule.repeat(schedule.every().day.at('06:00'))
def get_metrics_day():
    exporter('veris', 'day')


# Экспорт Юг
@schedule.repeat(schedule.every().day.at('04:00'))
def get_metrics_day():
    exporter('south', 'day')


# Экспорт Щелково
@schedule.repeat(schedule.every().day.at('03:00'))
def get_metrics_day():
    exporter('msk-sch', 'day')


# Экспорт Сергиев-Посад
@schedule.repeat(schedule.every().day.at('05:00'))
def get_metrics_day():
    exporter('sergpas', 'day')


# Экспорт Владикавказ
@schedule.repeat(schedule.every().day.at('07:00'))
def get_metrics_day():
    exporter('vkz', 'day')


# Экспорт Петергоф
@schedule.repeat(schedule.every().day.at('02:00'))
def get_metrics_day():
    exporter('vkus', 'day')


# Экспорт Корсаков
@schedule.repeat(schedule.every().day.at('14:03'))
def get_metrics_day():
    exporter('korsakov', 'day')


# Экспорт Омск
@schedule.repeat(schedule.every().day.at('01:00'))
def get_metrics_day():
    exporter('omsk', 'day')


# Экспорт Зеленогорск
@schedule.repeat(schedule.every().day.at('10:49'))
def get_metrics_day():
    dt = date(2022, 7, 5)
    while dt != date(2022, 7, 6):
        exporter('zelen', 'day', dt)
        work('zelen', 'day', dt)
        print(dt)
        dt += timedelta(days=1)


# Запись в базу данных Вересов
@schedule.repeat(schedule.every().day.at('06:05'))
def get_metrics_day():
    work('veris', 'day')


# Запись в базу данных Юг
@schedule.repeat(schedule.every().day.at('04:10'))
def get_metrics_day():
    work('south', 'day')


# Запись в базу данных Щелково
@schedule.repeat(schedule.every().day.at('03:10'))
def get_metrics_day():
    work('msk-sch', 'day')


# Запись в базу данных Сергиев-Посад
@schedule.repeat(schedule.every().day.at('05:05'))
def get_metrics_day():
    work('sergpas', 'day')


# Запись в базу данных Владикавказ
@schedule.repeat(schedule.every().day.at('07:05'))
def get_metrics_day():
    work('vkz', 'day')


# Запись в базу данных Петергоф
@schedule.repeat(schedule.every().day.at('02:20'))
def get_metrics_day():
    work('vkus', 'day')


# Запись в базу данных Корсаков
@schedule.repeat(schedule.every().day.at('14:08'))
def get_metrics_day():
    work('korsakov', 'day')


# Запись в базу данных Омск
@schedule.repeat(schedule.every().day.at('01:10'))
def get_metrics_day():
    work('omsk', 'day')


# Запись в базу данных Зеленогорск
@schedule.repeat(schedule.every().day.at('01:10'))
def get_metrics_day():
    work('zelen', 'day')


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
