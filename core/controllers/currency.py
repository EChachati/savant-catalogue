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

        if not obj.updated_at or (
            obj.updated_at.date() < date.today()
            and datetime.date.today().weekday() < 5
        ):
            response = requests.get(self.url)

            data = response.json()
            obj.to_usd = data["conversion_rates"][code.upper()]
            obj.updated_at = datetime.now()
            obj = self.crud.update(obj)
        return obj
