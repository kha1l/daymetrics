from postgres.psql import Database
from application.reader import ReadFile


def writer(group: int, tps: str):
    db = Database()
    users = db.get_users(group)
    for user in users:
        file = ReadFile(user[0], tps)
        df_rev = file.open_file('revenue', 17)
        df_prod = file.open_file('productivity', 4)
        df_del = file.open_file('del_statistic', 5)
