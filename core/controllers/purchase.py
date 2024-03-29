from collections import Counter

from sqlmodel_crud_manager.crud import CRUDManager

from core.api.product import crud as product_crud
from core.controllers.whatsapp import link_generator
from core.sql.database import engine
from core.sql.models.purchase import (
    Purchase,
    PurchaseCreate,
    PurchaseResponse,
)
from core.sql.models.purchase_product_link import PurchaseProductLink


class PurchaseController:
    def __init__(self):
        self.crud = CRUDManager(Purchase, engine)
        self.product_crud = product_crud

    def get(self, pk: int) -> PurchaseResponse:
        obj = PurchaseResponse.model_validate(self.crud.get(pk))
        obj.total_usd = sum([link.amount for link in obj.products_purchased])
        return obj

    def create(self, purchase: PurchaseCreate):
        purchase_obj = self.crud.create(purchase)

        product_ids = purchase.product_ids
        products = self.product_crud.get_by_ids(
            product_ids,
            self.crud.db,
        )

        quantities = dict(Counter(purchase.product_ids))

        for product in products:
            self.crud.db.add(
                PurchaseProductLink(
                    purchase_id=purchase_obj.id,
                    product_id=product.id,
                    quantity=quantities[product.id],
                    amount=quantities[product.id] * product.price,
                )
            )
        self.crud.db.commit()
        return self.get(purchase_obj.id)

    def list(self):
        return self.crud.list()

    def update(self, purchase: PurchaseCreate):
        raise NotImplementedError

    def delete(self, pk: int):
        raise NotImplementedError

    def get_as_message(self, pk: int):
        purchase = self.crud.get(pk)

        return link_generator(
            phone_number=purchase.company.phone,
            text=purchase.as_message(),
        )
