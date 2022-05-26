import psycopg2
from config.conf import Config


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
        sql = 'SELECT name_rest FROM settingsrest WHERE group_index=%s order by rest_id;'
        parameters = (group,)
        return self.execute(sql, parameters=parameters, fetchall=True)
