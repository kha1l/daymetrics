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
            print('change_time - attribute')
            t = timedelta(0)
        return t

    @staticmethod
    def df_handover(df):
        def change_time(t):
            try:
                t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            except AttributeError:
                print('change_time - attribute')
                t = timedelta(0)
            return t

        try:
            time_handover = pd.to_timedelta(
                df['Ожидание'].apply(change_time).mean() + df['Приготовление'].apply(change_time).mean())
        except KeyError:
            print('Ожидание or Приготовление - key')
            time_handover = '0:00:00'

        if issubclass(type(time_handover), pd._libs.tslibs.nattype.NaTType):
            time_handover = pd.to_timedelta(0)

        return time_handover

    def change_revenue(self):
        df = self.obj.df_rev

        try:
            revenue = df.iloc[0]['Итого']
        except IndexError:
            print('Выручка - index')
            revenue = 0
        except KeyError:
            print('Выручка - key')
            revenue = 0

        try:
            revenue_rest = df.iloc[0]['Ресторан']
        except IndexError:
            print('Выручка ресторана - index')
            revenue_rest = 0
        except KeyError:
            print('Выручка ресторана - key')
            revenue_rest = 0

        return int(revenue), int(revenue_rest)

    def change_productivity(self):
        df = self.obj.df_prod

        try:
            productivity = int(df.iloc[0]['Выручка на человека в час'])
        except IndexError:
            print('Выручка на человека в час - index')
            productivity = 0
        except KeyError:
            print('Выручка на человека в час - key')
            productivity = 0

        try:
            order_per_hour = df.iloc[0]['Кол-во заказов на курьера в час']
        except IndexError:
            print('Заказов на курьера в час - index')
            order_per_hour = 0
        except KeyError:
            print('Заказов на курьера в час - key')
            order_per_hour = 0

        try:
            product_on_hour = df.iloc[0]['Продуктов на человека в час']
        except IndexError:
            print('Продуктов на человека в час - index')
            product_on_hour = 0
        except KeyError:
            print('Продуктов на человека в час - key')
            product_on_hour = 0

        return int(productivity), float(product_on_hour), float(order_per_hour)

    def change_prepare(self):
        df = self.obj.df_prepare
        try:
            prepare = float(round(df['Стоимость'].sum() + df['Сумма'].sum(), 2))
        except KeyError:
            prepare = 0
        return prepare

    def change_scrap(self):
        df = self.obj.df_scrap
        try:
            scrap = float(round(df['Стоимость'].sum() + df['Сумма'].sum(), 2))
        except KeyError:
            scrap = 0
        return scrap

    def change_being_stop(self):
        df = self.obj.df_stop

        try:
            df = df.drop_duplicates(subset=['Дата остановки'], keep='first')
        except KeyError:
            print('Дата остановки - key')
            df = 0

        try:
            stop_duration = pd.to_timedelta(df['Длительность за отчетный период'].apply(self.change_time).sum())
        except KeyError:
            print('Длительность за отчетный период - key')
            stop_duration = 0

        try:
            df = df.drop_duplicates(subset=['Причина остановки'], keep='first')
        except KeyError:
            print('Причина остановки - key')
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
            print('Среднее время доставки* - index')
            avg_del = timedelta(0)
        except KeyError:
            print('Среднее время доставки* - key')
            avg_del = timedelta(0)

        try:
            cert = df.iloc[0]['Количество просроченных заказов']
        except IndexError:
            print('Количество просроченных заказов - index')
            cert = 0
        except KeyError:
            print('Количество просроченных заказов - key')
            cert = 0

        return avg_del, int(cert)

    def change_handover_delivery(self):
        df = self.obj.df_hand_del

        def change_time(t):
            try:
                t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            except AttributeError:
                print('change_time - attribute')
                t = timedelta(0)
            return t

        try:
            time_shelf = pd.to_timedelta(df['Ожидание на полке'].apply(change_time).mean())
        except KeyError:
            print('Ожидание на полке - key')
            time_shelf = timedelta(0)

        if issubclass(type(time_shelf), pd._libs.tslibs.nattype.NaTType):
            time_shelf = pd.to_timedelta(0)

        handover = self.df_handover(df)

        return handover, time_shelf

    def change_handover_stationary(self):
        df = self.obj.df_hand_stat

        handover = self.df_handover(df)

        return handover
