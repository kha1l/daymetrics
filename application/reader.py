import pandas as pd


class ReadFile:

    def __init__(self, name_rest: str, tps: str):
        self.name = name_rest
        self.tps = tps

    def open_file(self, order: str, rows: int):
        df = pd.read_excel(f'./orders/export/{order}_{self.name}_{self.tps}.xlsx', skiprows=rows)
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

    def read_df(self):
        print('sfa')
        self.df_rev = self.open_file('revenue', 17)
        self.df_prod = self.open_file('productivity', 4)
        self.df_del = self.open_file('del_statistic', 5)
        self.df_stop = self.open_file('being_stop', 1)
        self.df_hand_del = self.open_file('handover-delivery', 2)
        self.df_hand_stat = self.open_file('handover_stationary', 3)
        self.df_prepare = self.open_file('prepare', 4)
        self.df_scrap = self.open_file('scrap', 5)
