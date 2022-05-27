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
        sql = 'SELECT rest_id, long_id, login, password FROM settingsrest WHERE name_rest=%s;'
        parameters = (name,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_users(self, group: int):
        sql = 'SELECT name_rest, rest_id FROM settingsrest WHERE group_index=%s order by rest_id;'
        parameters = (group,)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_line(self, dt: str, rest_id: int):
        sql = 'SELECT date, rest_id FROM daymetrics WHERE date=%s and rest_id=%s'
        parameters = dt, rest_id
        return self.execute(sql, parameters=parameters, fetchall=True)

    def add_metrics(self, dt: date, rest_id: int, name_rest: str, revenue: int, revenue_rest: int,
                    productivity: int, orders_per_hour: float, product: float, time_in_rest: timedelta,
                    time_in_delivery: timedelta, time_in_shelf: timedelta, delivery_time: timedelta,
                    stop_selling: timedelta, cause_of_stops: str, certificates: int, prepare: float, scrap: float):
        sql = '''
            INSERT INTO daymetrics (
                date, rest_id, name_rest, revenue,
                revenue_rest, productivity, orders_per_hour,
                product, time_in_rest, time_in_delivery,
                time_in_shelf, delivery_time, stop_selling, cause_of_stops,
                certificates, prepare, scrap) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            )
        '''
        parameters = (dt, rest_id, name_rest, revenue, revenue_rest, productivity, orders_per_hour, product,
                      time_in_rest, time_in_delivery, time_in_shelf, delivery_time, stop_selling, cause_of_stops,
                      certificates, prepare, scrap)
        self.execute(sql, parameters=parameters, commit=True)

    def update_metrics(self, dt: date, rest_id: int, name_rest: str, revenue: int, revenue_rest: int,
                       productivity: int, orders_per_hour: float, product: float, time_in_rest: timedelta,
                       time_in_delivery: timedelta, time_in_shelf: timedelta, delivery_time: timedelta,
                       stop_selling: timedelta, cause_of_stops: str, certificates: int, prepare: float, scrap: float):
        sql = '''
            UPDATE daymetrics SET date=%s, rest_id=%s, name_rest=%s, revenue=%s,
                revenue_rest=%s, productivity=%s, orders_per_hour=%s,
                product=%s, time_in_rest=%s, time_in_delivery=%s,
                time_in_shelf=%s, delivery_time=%s, stop_selling=%s, cause_of_stops=%s,
                certificates=%s, prepare=%s, scrap=%s WHERE date=%s AND rest_id=%s
        '''
        parameters = (dt, rest_id, name_rest, revenue, revenue_rest, productivity, orders_per_hour, product,
                      time_in_rest, time_in_delivery, time_in_shelf, delivery_time, stop_selling, cause_of_stops,
                      certificates, prepare, scrap, dt, rest_id)
        self.execute(sql, parameters=parameters, commit=True)
