from postgres.psql import Database
from application.reader import Reader
from application.changer import Changer
from date_work import DataWork


def work(group: str, tps: str):
    db = Database()
    users = db.get_users(group)
    dt = DataWork().set_date()
    for user in users:
        line = db.get_line(dt, user[1])
        cls_df = Reader(user[0], tps)
        cls_df.read_df()
        change = Changer(cls_df)
        revenue, revenue_rest = change.change_revenue()
        productivity, product, orders_per_hour = change.change_productivity()
        prepare, proc_prepare = change.change_prepare(revenue)
        scrap, proc_scrap = change.change_scrap(revenue)
        stop_selling, cause_of_stops = change.change_being_stop()
        delivery_time, certificates = change.change_delivery_statistic()
        time_in_delivery, time_in_shelf = change.change_handover_delivery()
        time_in_rest = change.change_handover_stationary()
        if len(line) == 0:
            db.add_metrics(dt, user[1], user[0], revenue, revenue_rest, productivity, orders_per_hour, product,
                           time_in_rest, time_in_delivery, time_in_shelf, delivery_time, stop_selling, cause_of_stops,
                           certificates, prepare, proc_prepare, scrap, proc_scrap)
        else:
            db.update_metrics(dt, user[1], user[0], revenue, revenue_rest, productivity, orders_per_hour, product,
                              time_in_rest, time_in_delivery, time_in_shelf, delivery_time, stop_selling,
                              cause_of_stops, certificates, prepare, proc_prepare, scrap, proc_scrap)
