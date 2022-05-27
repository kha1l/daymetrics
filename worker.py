from postgres.psql import Database
from application.reader import Reader
from application.changer import Changer


def work(group: int, tps: str):
    db = Database()
    users = db.get_users(group)
    for user in users:
        cls_df = Reader(user[0], tps)
        cls_df.read_df()
        change = Changer(cls_df)
