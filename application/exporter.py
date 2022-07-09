from postgres.psql import Database
from orders.export import DataExportDay
from date_work import DataWork
import time


def exporter(group: str, tps: str):
    db = Database()
    dt = DataWork().set_date()
    users = db.get_users(group)
    for user in users:
        data = DataExportDay(dt, user[0], tps)
        data.productivity()
        data.revenue()
        data.delivery_statistic()
        data.being_stop()
        data.handover_delivery()
        data.handover_stationary()
        data.prepare()
        data.scrap()
        data.prepare_case()
        data.average_check()
        time.sleep(5)
