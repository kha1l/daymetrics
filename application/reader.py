import pandas as pd


class ReadFile:

    def __init__(self, name_rest: str, tps: str):
        self.name = name_rest
        self.tps = tps

    def open_file(self, order: str, rows: int):
        try:
            df = pd.read_excel(f'./orders/export/{order}_{self.name}_{self.tps}.xlsx', skiprows=rows)
        except ValueError:
            df = pd.DataFrame()
        return df

    def open_file_prepare(self, order: str, rows: int):
        try:
            df = pd.read_excel(f'./orders/export/{order}_{self.name}_{self.tps}.xlsx', sheet_name='Исходные данные',
                               skiprows=rows)
        except ValueError:
            df = pd.DataFrame()
        return df


class Reader(ReadFile):

    df_rev = None
    df_prod = None
    df_del = None
    df_stop = None
    df_hand_del = None
    df_hand_stat = None
    df_prepare = None
    df_scrap = None
    df_prepareCase = None
    df_avgCheck = None
    df_rating_client = None

    def read_df(self):
        self.df_rev = self.open_file('revenue', 17)
        self.df_prod = self.open_file('productivity', 4)
        self.df_del = self.open_file('del_statistic', 5)
        self.df_stop = self.open_file('being_stop', 5)
        self.df_hand_del = self.open_file('handover-delivery', 6)
        self.df_hand_stat = self.open_file('handover_stationary', 6)
        self.df_prepare = self.open_file_prepare('prepare', 0)
        self.df_scrap = self.open_file_prepare('scrap', 0)
        self.df_prepareCase = self.open_file_prepare('prepare_case', 0)
        self.df_avgCheck = self.open_file('average_check', 7)
        self.df_rating_client = pd.read_json('https://publicapi.dodois.io/ru/api/v1/ratings')
