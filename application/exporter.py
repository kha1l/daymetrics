from postgres.psql import Database
from orders.export import DataExportDay
from date_work import DataWork
import time


def exporter(group: str, tps: str):
    db = Database()
    dt = DataWork().set_date()
    users = db.get_users(group)
    for user in users:
        data = DataExportDay(dt, user[0])
        data.productivity(tps)
        data.revenue(tps)
        data.delivery_statistic(tps)
        data.being_stop(tps)
        data.handover_delivery(tps)
        data.handover_stationary(tps)
        data.prepare(tps)
        data.scrap(tps)
        time.sleep(30)
