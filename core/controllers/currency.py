import os
from datetime import date, datetime

import requests
from dotenv import load_dotenv
from sqlmodel_crud_manager.crud import CRUDManager

from core.sql.database import engine
from core.sql.models.generic import Currency

load_dotenv()


class CurrencyController:
    def __init__(self):
        self.crud = CRUDManager(Currency, engine)
        self.url = f"https://v6.exchangerate-api.com/v6/{os.environ["EXCHANGERATES_API_KEY"]}/latest/USD"

    def get_by_code(self, code: str) -> Currency:
        obj: Currency = self.crud.get_by_field(field="code", value=code)
        print("xd")
        if not obj.updated_at or (
            obj.updated_at.date() < date.today() and date.today().weekday() < 5
        ):
            response = requests.get(self.url)

            data = response.json()
            obj.to_usd = data["conversion_rates"][code.upper()]
            obj.updated_at = datetime.now()
            obj = self.crud.update(obj)
        return obj


__VES_CURRENCY: Currency = CurrencyController().get_by_code("VES")


def get_ves_currency():
    global __VES_CURRENCY
    if not __VES_CURRENCY.updated_at or (
        __VES_CURRENCY.updated_at.date() < date.today()
        and date.today().weekday() < 5
    ):
        __VES_CURRENCY = CurrencyController().get_by_code("VES")
    return __VES_CURRENCY
