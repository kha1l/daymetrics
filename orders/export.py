import requests
import fake_useragent
from datetime import date, timedelta
from postgres.psql import Database


class DataExportDay:

    def __init__(self, date_end: date, name: str):
        db = Database()
        data = db.get_data(name)
        self.name = name
        self.rest = data[0]
        self.uuid = data[1]
        self.date_end = date_end
        self.login = data[2]
        self.password = data[3]
        self.code = data[4]
        self.session = None
        self.user = None
        self.header = None
        self.tps = None
        self.auth()

    def auth(self):
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
        log_data = {
            'CountryCode': self.code,
            'login': self.login,
            'password': self.password
        }
        self.header = {
            'user-agent': self.user
        }
        log_link = f'https://auth.dodopizza.{self.code}/Authenticate/LogOn'
        self.session.post(log_link, data=log_data, headers=self.header)

    def save(self, orders_data):
        for order in orders_data:
            response = self.session.post(orders_data[order]['link'], data=orders_data[order]['data'],
                                         headers=self.header)
            with open(f'./orders/export/{order}_{self.name}_{self.tps}.xlsx', 'wb') as file:
                file.write(response.content)
                file.close()

    def productivity(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'productivity': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/Productivity/Export',
                'data': {
                    "unitId": self.rest,
                    "beginDate": self.date_end - timedelta(days=delta_days[tps]),
                    "endDate": self.date_end,
                    "Interval": "24"
                }
            }
        }
        self.save(orders_data)

    def revenue(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'revenue': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/Revenue/Export',
                'data': {
                    "unitsIds": self.rest,
                    "OrderSources": [
                        "Telephone",
                        "Site",
                        "Restaurant",
                        "Mobile",
                        "Pizzeria",
                        "Aggregator"
                    ],
                    "ReportType": "ByDates",
                    "reportType": "",
                    "pseudoBeginTime": "",
                    "pseudoBeginDate": self.date_end - timedelta(days=delta_days[tps]),
                    "pseudoEndTime": "",
                    "pseudoEndDate": self.date_end,
                    "beginDate": self.date_end - timedelta(days=delta_days[tps]),
                    "endDate": self.date_end,
                    "beginTime": "",
                    "endTime": "",
                    "date": self.date_end,
                    "IsVatIncluded": [
                        "true",
                        "false"
                    ],
                    "Export": "Экспорт+в+Excel"
                }
            }
        }
        self.save(orders_data)

    def delivery_statistic(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'del_statistic': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/DeliveryStatistic/Export',
                'data': {
                    "unitsIds": self.rest,
                    "beginDate": self.date_end - timedelta(days=delta_days[tps]),
                    "endDate": self.date_end
                }
            }
        }
        self.save(orders_data)

    def being_stop(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'being_stop': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/StopSaleStatistic/Export',
                'data': {
                    "UnitsIds": self.rest,
                    "stopType": "0",
                    "beginDate": self.date_end - timedelta(days=delta_days[tps]),
                    "endDate": self.date_end
                }
            }
        }
        self.save(orders_data)

    def handover_delivery(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'handover-delivery': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/OrderHandoverTime/Export',
                'data': {
                    "unitsIds": self.uuid,
                    "beginDate": self.date_end - timedelta(days=delta_days[tps]),
                    "endDate": self.date_end,
                    "orderTypes": "Delivery",
                    "Export": "Экспорт+в+Excel"
                }
            }
        }
        self.save(orders_data)

    def handover_stationary(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'handover_stationary': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/OrderHandoverTime/Export',
                'data': {
                    "unitsIds": self.uuid,
                    "beginDate": self.date_end - timedelta(days=delta_days[tps]),
                    "endDate": self.date_end,
                    "orderTypes": "Stationary",
                    "Export": "Экспорт+в+Excel"
                }
            }
        }
        self.save(orders_data)

    def prepare(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'prepare': {
                'link': f'https://officemanager.dodopizza.{self.code}/OfficeManager/Debiting/BuildExcelReport',
                'data': {
                    "DebitingReasonId": [
                        "100",
                        "500",
                        "600"
                    ],
                    "UnitId": self.rest,
                    "StartDate": self.date_end - timedelta(days=delta_days[tps]),
                    "EndDate": self.date_end,
                    "Mode": "ByDay",
                }
            }
        }
        self.save(orders_data)

    def scrap(self, tps: str):
        self.tps = tps
        delta_days = {
            'day': 0,
            'week': 6,
        }
        orders_data = {
            'scrap': {
                'link': f'https://officemanager.dodopizza.{self.code}/OfficeManager/Debiting/BuildExcelReport',
                'data': {
                    "DebitingReasonId": [
                        "200",
                        "300",
                        "400",
                        "700"
                    ],
                    "UnitId": self.rest,
                    "StartDate": self.date_end - timedelta(days=delta_days[tps]),
                    "EndDate": self.date_end,
                    "Mode": "ByDay",
                }
            }
        }
        self.save(orders_data)
