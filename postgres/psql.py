import psycopg2
from config.conf import Config
from datetime import timedelta, date


class Database:
    @property
    def connection(self):
        cfg = Config()
        return psycopg2.connect(
            database=cfg.dbase,
            user=cfg.user,
            password=cfg.password,
            host=cfg.host,
            port='5432'
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def get_data(self, name: str):
        sql = 'SELECT restId, uuId, restLogin, restPassword, countryCode FROM settings WHERE restName=%s;'
        parameters = (name,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_users(self, group: str):
        sql = 'SELECT restName, restId FROM settings WHERE restGroup=%s order by restId;'
        parameters = (group,)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_line(self, dt: str, rest_id: int):
        sql = 'SELECT ordersDay, restId FROM day WHERE ordersDay=%s and restId=%s'
        parameters = (dt, rest_id)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def add_metrics(self, dt: date, rest_id: int, name_rest: str, revenue: int, revenue_rest: int,
                    productivity: int, orders_per_hour: float, product: float, time_in_rest: timedelta,
                    time_in_delivery: timedelta, time_in_shelf: timedelta, delivery_time: timedelta,
                    stop_selling: timedelta, cause_of_stops: str, certificates: int, prepare: float,
                    proc_prepare: float, prepare_case: float, scrap: float, proc_scrap: float, sp_kitchen: float,
                    revenue_del: int, revenue_pick: int, check_del: float, check_rest: float):
        sql = '''
            INSERT INTO day (
                ordersDay, restId, restName, revenue,
                revenueRest, productivity, ordersHour,
                productHour, timeRest, timeDelivery,
                timeShelf, speedDelivery, stopSelling, stopCause,
                certificates, prepares, preparesPercent, prepareShowcase, 
                scraps, scrapsPercent, speedKitchen, revenueDelivery, revenuePickup, 
                checkDelivery, checkrest) 
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s
            )
        '''
        parameters = (dt, rest_id, name_rest, revenue, revenue_rest, productivity, orders_per_hour, product,
                      time_in_rest, time_in_delivery, time_in_shelf, delivery_time, stop_selling, cause_of_stops,
                      certificates, prepare, proc_prepare, prepare_case, scrap, proc_scrap, sp_kitchen,
                      revenue_del, revenue_pick, check_del, check_rest)
        self.execute(sql, parameters=parameters, commit=True)

    def update_metrics(self, dt: date, rest_id: int, name_rest: str, revenue: int, revenue_rest: int,
                       productivity: int, orders_per_hour: float, product: float, time_in_rest: timedelta,
                       time_in_delivery: timedelta, time_in_shelf: timedelta, delivery_time: timedelta,
                       stop_selling: timedelta, cause_of_stops: str, certificates: int, prepare: float,
                       proc_prepare: float, prepare_case: float, scrap: float, proc_scrap: float, sp_kitchen: float,
                       revenue_del: int, revenue_pick: int, check_del: float, check_rest: float):
        sql = '''
            UPDATE day SET ordersDay=%s, restId=%s, restName=%s, revenue=%s,
                revenueRest=%s, productivity=%s, ordersHour=%s,
                productHour=%s, timeRest=%s, timeDelivery=%s,
                timeShelf=%s, speedDelivery=%s, stopSelling=%s, stopCause=%s,
                certificates=%s, prepares=%s, preparesPercent=%s, 
                prepareShowcase=%s, scraps=%s, scrapsPercent=%s, speedKitchen=%s,
                revenueDelivery=%s, revenuePickup=%s , checkDelivery=%s, checkRest=%s
                WHERE ordersDay=%s AND restId=%s
        '''
        parameters = (dt, rest_id, name_rest, revenue, revenue_rest, productivity, orders_per_hour, product,
                      time_in_rest, time_in_delivery, time_in_shelf, delivery_time, stop_selling, cause_of_stops,
                      certificates, prepare, proc_prepare, prepare_case, scrap, proc_scrap, sp_kitchen,
                      revenue_del, revenue_pick, check_del, check_rest, dt, rest_id)
        self.execute(sql, parameters=parameters, commit=True)
