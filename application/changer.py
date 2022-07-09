from application.reader import Reader
from datetime import timedelta
import pandas as pd


class Changer:

    def __init__(self, obj: Reader) -> None:
        self.obj = obj

    @staticmethod
    def change_time(t):
        try:
            t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
        except AttributeError:
            t = timedelta(0)
        return t

    @staticmethod
    def df_handover(df):
        def change_time(t):
            try:
                t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            except AttributeError:
                t = timedelta(0)
            return t

        try:
            time_handover = pd.to_timedelta(
                df['Ожидание'].apply(change_time).mean() + df['Приготовление'].apply(change_time).mean())
        except KeyError:
            time_handover = '0:00:00'

        if issubclass(type(time_handover), pd._libs.tslibs.nattype.NaTType):
            time_handover = pd.to_timedelta(0)

        return time_handover

    def change_revenue(self):
        df = self.obj.df_rev

        try:
            revenue = df.iloc[0]['Итого']
        except IndexError:
            revenue = 0
        except KeyError:
            revenue = 0

        try:
            revenue_rest = df.iloc[0]['Ресторан']
        except IndexError:
            revenue_rest = 0
        except KeyError:
            revenue_rest = 0

        try:
            revenue_del = df.iloc[0]['Доставка']
        except IndexError:
            revenue_del = 0
        except KeyError:
            revenue_del = 0

        try:
            revenue_pick = df.iloc[0]['Самовывоз']
        except IndexError:
            revenue_pick = 0
        except KeyError:
            revenue_pick = 0

        return int(revenue), int(revenue_rest), int(revenue_del), int(revenue_pick)

    def change_productivity(self):
        df = self.obj.df_prod

        try:
            productivity = int(df.iloc[0]['Выручка на человека в час'])
        except IndexError:
            productivity = 0
        except KeyError:
            productivity = 0

        try:
            order_per_hour = df.iloc[0]['Кол-во заказов на курьера в час']
        except IndexError:
            order_per_hour = 0
        except KeyError:
            order_per_hour = 0

        try:
            product_on_hour = df.iloc[0]['Продуктов на человека в час']
        except IndexError:
            product_on_hour = 0
        except KeyError:
            product_on_hour = 0

        try:
            speed_kitchen = round(float(df.iloc[0]['Скорость']), 2)
        except IndexError:
            speed_kitchen = 0
        except KeyError:
            speed_kitchen = 0

        return int(productivity), float(product_on_hour), float(order_per_hour), speed_kitchen

    def change_prepare(self, revenue):
        df = self.obj.df_prepare
        try:
            prepare = float(round(df['Сумма'].sum(), 2))
        except KeyError:
            prepare = 0
        try:
            proc_prepare = float(round(prepare / revenue, 3))
        except ZeroDivisionError:
            proc_prepare = 0
        return prepare, proc_prepare

    def change_prepare_case(self):
        df = self.obj.df_prepareCase
        try:
            prepare_case = float(round(df['Сумма'].sum(), 2))
        except KeyError:
            prepare_case = 0
        return prepare_case

    def change_scrap(self, revenue):
        df = self.obj.df_scrap
        try:
            scrap = float(round(df['Сумма'].sum(), 2))
        except KeyError:
            scrap = 0
        try:
            proc_scrap = float(round(scrap / revenue, 3))
        except ZeroDivisionError:
            proc_scrap = 0
        return scrap, proc_scrap

    def change_being_stop(self):
        df = self.obj.df_stop

        try:
            df = df.drop_duplicates(subset=['Дата остановки'], keep='first')
        except KeyError:
            df = 0

        try:
            stop_duration = pd.to_timedelta(df['Длительность за отчетный период'].apply(self.change_time).sum())
        except KeyError:
            stop_duration = 0

        try:
            df = df.drop_duplicates(subset=['Причина остановки'], keep='first')
        except KeyError:
            df = 0

        try:
            cause_stop = df['Причина остановки'].tolist()
        except KeyError:
            cause_stop = 0

        if len(cause_stop) != 0:
            stop_cause = ','.join(cause_stop)
        else:
            stop_cause = '-'

        return stop_duration, stop_cause

    def change_delivery_statistic(self):
        df = self.obj.df_del

        try:
            avg_del = df.iloc[0]['Среднее время доставки*']
        except IndexError:
            avg_del = timedelta(0)
        except KeyError:
            avg_del = timedelta(0)

        try:
            cert = df.iloc[0]['Количество просроченных заказов']
        except IndexError:
            cert = 0
        except KeyError:
            cert = 0

        return avg_del, int(cert)

    def change_handover_delivery(self):
        df = self.obj.df_hand_del

        def change_time(t):
            try:
                t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            except AttributeError:
                t = timedelta(0)
            return t

        try:
            time_shelf = pd.to_timedelta(df['Ожидание на полке'].apply(change_time).mean())
        except KeyError:
            time_shelf = timedelta(0)

        if issubclass(type(time_shelf), pd._libs.tslibs.nattype.NaTType):
            time_shelf = pd.to_timedelta(0)

        handover = self.df_handover(df)

        return handover, time_shelf

    def change_handover_stationary(self):
        df = self.obj.df_hand_stat

        handover = self.df_handover(df)

        return handover

    def change_check(self):
        df = self.obj.df_avgCheck

        try:
            check_del = round(float(df.iloc[0]['Средний чек']), 2)
        except IndexError:
            check_del = 0
        except KeyError:
            check_del = 0

        try:
            check_rest = round(float(df.iloc[0]['Средний чек.1']), 2)
        except IndexError:
            check_rest = 0
        except KeyError:
            check_rest = 0

        return check_del, check_rest

    def change_rating_client(self, uuid):
        df = self.obj.df_rating_client
        df_rat = df.loc[df['UnitUUId'] == uuid].reset_index()
        try:
            rating = round(df_rat.iloc[0]['AvgRating'], 2)
        except IndexError:
            rating = 0
        return float(rating)

